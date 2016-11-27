from __future__ import unicode_literals
import logging
from .storage import StorageAdapter
from .logic import LogicAdapter, MultiLogicAdapter
from .input import InputAdapter
from .output import OutputAdapter
from .conversation.session import SessionManager
from .utils import import_module


class ChatBot(object):
    """
    A conversational dialog ChatBot.
    """

    def __init__(self, name, **kwargs):
        self.name = name
        kwargs['name'] = name

        storage_adapter = kwargs.get('storage_adapter', 'chatterbot.storage.JsonFileStorageAdapter')

        logic_adapters = kwargs.get('logic_adapters', [
            'chatterbot.logic.ClosestMatchAdapter'
        ])

        input_adapter = kwargs.get('input_adapter', 'chatterbot.input.VariableInputTypeAdapter')

        output_adapter = kwargs.get('output_adapter', 'chatterbot.output.OutputFormatAdapter')

        # The storage adapter must be an instance of StorageAdapter
        self.validate_adapter_class(storage_adapter, StorageAdapter)

        # The input adapter must be an instance of InputAdapter
        self.validate_adapter_class(input_adapter, InputAdapter)

        # The output adapter must be an instance of OutputAdapter
        self.validate_adapter_class(output_adapter, OutputAdapter)

        self.logic = MultiLogicAdapter(**kwargs)
        self.storage = self.initialize_class(storage_adapter, **kwargs)
        self.input = self.initialize_class(input_adapter, **kwargs)
        self.output = self.initialize_class(output_adapter, **kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = (import_module(F)() for F in filters)

        # Add required system logic adapter
        self.add_logic_adapter('chatterbot.logic.NoKnowledgeAdapter')

        for adapter in logic_adapters:
            self.add_logic_adapter(adapter, **kwargs)

        # Add the chatbot instance to each adapter to share information such as
        # the name, the current conversation, or other adapters
        self.storage.set_chatbot(self)
        self.logic.set_chatbot(self)
        self.input.set_chatbot(self)
        self.output.set_chatbot(self)

        # Use specified trainer or fall back to the default
        trainer = kwargs.get('trainer', 'chatterbot.trainers.Trainer')
        TrainerClass = import_module(trainer)
        self.trainer = TrainerClass(self.storage, **kwargs)
        self.training_data = kwargs.get('training_data')

        self.conversation_sessions = SessionManager()
        self.default_session = self.conversation_sessions.new()

        self.logger = kwargs.get('logger', logging.getLogger(__name__))
        self.initialize()

    def initialize(self):
        """
        Do any work that needs to be done before the responses can be returned.
        """
        from .utils import nltk_download_corpus

        # Download the stopwords data only if it is not already downloaded
        nltk_download_corpus('stopwords')

        # Download the wordnet data only if it is not already downloaded
        nltk_download_corpus('wordnet')

        # Download the punkt data only if it is not already downloaded
        nltk_download_corpus('punkt')

    def initialize_class(self, adapter_data, **kwargs):
        """
        :param adapter_data: A string or dictionary containing a import_path attribute.
        """
        if isinstance(adapter_data, dict):
            import_path = adapter_data.pop('import_path')
            adapter_data.update(kwargs)
            Class = import_module(import_path)

            return Class(**adapter_data)
        else:
            Class = import_module(adapter_data)

            return Class(**kwargs)

    def add_logic_adapter(self, adapter, **kwargs):
        """
        Add a logic adapter to the chat bot.
        """
        self.validate_adapter_class(adapter, LogicAdapter)
        adapter = self.initialize_class(adapter, **kwargs)
        self.logic.add_adapter(adapter)

    def insert_logic_adapter(self, logic_adapter, insert_index, **kwargs):
        """
        Adds a logic adapter at a specified index.

        :param logic_adapter: The string path to the logic adapter to add.
        :type logic_adapter: class

        :param insert_index: The index to insert the logic adapter into the list at.
        :type insert_index: int

        :raises: InvalidAdapterException
        """
        self.validate_adapter_class(logic_adapter, LogicAdapter)

        NewAdapter = import_module(logic_adapter)
        adapter = NewAdapter(**kwargs)

        self.logic.adapters.insert(insert_index, adapter)

    def remove_logic_adapter(self, adapter_name):
        """
        Removes a logic adapter from the chat bot.

        :param adapter_name: The class name of the adapter to remove.
        :type adapter_name: str
        """
        for index, adapter in enumerate(self.logic.adapters):
            if adapter_name == type(adapter).__name__:
                del self.logic.adapters[index]
                return True
        return False

    def validate_adapter_class(self, validate_class, adapter_class):
        """
        Raises an exception if validate_class is not a
        subclass of adapter_class.

        :param validate_class: The class to be validated.
        :type validate_class: class

        :param adapter_class: The class type to check against.
        :type adapter_class: class

        :raises: InvalidAdapterException
        """
        from .adapters import Adapter

        # If a dictionary was passed in, check if it has an import_path attribute
        if isinstance(validate_class, dict):
            origional_data = validate_class.copy()
            validate_class = validate_class.get('import_path')

            if not validate_class:
                raise self.InvalidAdapterException(
                    'The dictionary {} must contain a value for "import_path"'.format(
                        str(origional_data)
                    )
                )

        if not issubclass(import_module(validate_class), Adapter):
            raise self.InvalidAdapterException(
                '{} must be a subclass of {}'.format(
                    validate_class,
                    Adapter.__name__
                )
            )

        if not issubclass(import_module(validate_class), adapter_class):
            raise self.InvalidAdapterException(
                '{} must be a subclass of {}'.format(
                    validate_class,
                    adapter_class.__name__
                )
            )

    def get_response(self, input_item, session_id=None):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :returns: A response to the input.
        :rtype: Statement
        """
        if not session_id:
            session_id = str(self.default_session.uuid)

        input_statement = self.input.process_input_statement(input_item)

        statement, response, confidence = self.generate_response(input_statement)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.conversation_sessions.get(
            session_id
        ).conversation.get_last_response_statement()
        self.learn_response(statement, previous_statement)

        self.conversation_sessions.update(session_id, (statement, response, ))

        # Process the response output with the output adapter
        return self.output.process_response(response, confidence, session_id)

    def generate_response(self, input_statement):
        """
        Return a response based on a given input statement.
        """
        self.storage.generate_base_query(self)

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)

        return input_statement, response, confidence

    def learn_response(self, statement, previous_statement):
        """
        Learn that the statement provided is a valid response.
        """
        from .conversation import Response

        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )
            self.logger.info('Adding "{}" as a response to "{}"'.format(
                statement.text,
                previous_statement.text
            ))

        # Update the database after selecting a response
        self.storage.update(statement)

    def set_trainer(self, training_class, **kwargs):
        """
        Set the module used to train the chatbot.

        :param training_class: The training class to use for the chat bot.
        :type training_class: chatterbot.trainers.Trainer

        :param \**kwargs: Any parameters that should be passed to the training class.
        """
        self.trainer = training_class(self.storage, **kwargs)

    @property
    def train(self):
        """
        Proxy method to the chat bot's trainer class.
        """
        return self.trainer.train

    @classmethod
    def from_config(cls, config_file_path):
        """
        Create a new ChatBot instance from a JSON config file.
        """
        import json
        with open(config_file_path, 'r') as config_file:
            data = json.load(config_file)

        name = data.pop('name')

        return ChatBot(name, **data)

    class InvalidAdapterException(Exception):
        """
        An exception to be raised when an adapter of an unexpected class type
        is recieved.
        """

        def __init__(self, value='Recieved an unexpected adapter setting.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
