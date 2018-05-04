from __future__ import unicode_literals
import logging
from .storage import StorageAdapter
from .input import InputAdapter
from .output import OutputAdapter
from . import utils


class ChatBot(object):
    """
    A conversational dialog chat bot.
    """

    def __init__(self, name, **kwargs):
        from .logic import MultiLogicAdapter

        self.name = name
        kwargs['name'] = name
        kwargs['chatbot'] = self

        self.default_session = None

        storage_adapter = kwargs.get('storage_adapter', 'chatterbot.storage.SQLStorageAdapter')

        # These are logic adapters that are required for normal operation
        system_logic_adapters = kwargs.get('system_logic_adapters', (
            'chatterbot.logic.NoKnowledgeAdapter',
        ))

        logic_adapters = kwargs.get('logic_adapters', [
            'chatterbot.logic.BestMatch'
        ])

        input_adapter = kwargs.get('input_adapter', 'chatterbot.input.VariableInputTypeAdapter')

        output_adapter = kwargs.get('output_adapter', 'chatterbot.output.OutputAdapter')

        # Check that each adapter is a valid subclass of it's respective parent
        utils.validate_adapter_class(storage_adapter, StorageAdapter)
        utils.validate_adapter_class(input_adapter, InputAdapter)
        utils.validate_adapter_class(output_adapter, OutputAdapter)

        self.logic = MultiLogicAdapter(**kwargs)
        self.storage = utils.initialize_class(storage_adapter, **kwargs)
        self.input = utils.initialize_class(input_adapter, **kwargs)
        self.output = utils.initialize_class(output_adapter, **kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = tuple([utils.import_module(F)() for F in filters])

        # Add required system logic adapter
        for system_logic_adapter in system_logic_adapters:
            self.logic.system_adapters.append(
                utils.initialize_class(system_logic_adapter, **kwargs)
            )

        for adapter in logic_adapters:
            self.logic.add_adapter(adapter, **kwargs)

        # Add the chatbot instance to each adapter to share information such as
        # the name, the current conversation, or other adapters
        self.logic.set_chatbot(self)
        self.input.set_chatbot(self)
        self.output.set_chatbot(self)

        preprocessors = kwargs.get(
            'preprocessors', [
                'chatterbot.preprocessors.clean_whitespace'
            ]
        )

        self.preprocessors = []

        for preprocessor in preprocessors:
            self.preprocessors.append(utils.import_module(preprocessor))

        # Use specified trainer or fall back to the default
        trainer = kwargs.get('trainer', 'chatterbot.trainers.Trainer')
        TrainerClass = utils.import_module(trainer)
        self.trainer = TrainerClass(self.storage, **kwargs)
        self.training_data = kwargs.get('training_data')

        self.default_conversation_id = None

        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        # Allow the bot to save input it receives so that it can learn
        self.read_only = kwargs.get('read_only', False)

        if kwargs.get('initialize', True):
            self.initialize()

    def initialize(self):
        """
        Do any work that needs to be done before the responses can be returned.
        """
        self.logic.initialize()

    def get_response(self, input_item, conversation_id=None):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :param conversation_id: The id of a conversation.
        :returns: A response to the input.
        :rtype: Statement
        """
        if not conversation_id:
            if not self.default_conversation_id:
                self.default_conversation_id = self.storage.create_conversation()
            conversation_id = self.default_conversation_id

        input_statement = self.input.process_input_statement(input_item)

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        statement, response = self.generate_response(input_statement, conversation_id)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.storage.get_latest_response(conversation_id)

        if not self.read_only:
            self.learn_response(statement, previous_statement)
            self.storage.add_to_conversation(conversation_id, statement, response)

        # Process the response output with the output adapter
        return self.output.process_response(response, conversation_id)

    def generate_response(self, input_statement, conversation_id):
        """
        Return a response based on a given input statement.
        """
        self.storage.generate_base_query(self, conversation_id)

        # Select a response to the input statement
        response = self.logic.process(input_statement)

        return input_statement, response

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

        # Save the statement after selecting a response
        self.storage.update(statement)

    def set_trainer(self, training_class, **kwargs):
        """
        Set the module used to train the chatbot.

        :param training_class: The training class to use for the chat bot.
        :type training_class: `Trainer`

        :param \**kwargs: Any parameters that should be passed to the training class.
        """
        if 'chatbot' not in kwargs:
            kwargs['chatbot'] = self

        self.trainer = training_class(self.storage, **kwargs)

    @property
    def train(self):
        """
        Proxy method to the chat bot's trainer class.
        """
        return self.trainer.train
