from .adapters.storage import StorageAdapter
from .adapters.logic import LogicAdapter, MultiLogicAdapter
from .adapters.input import InputAdapter
from .adapters.output import OutputAdapter
from .conversation import Statement, Response
from .utils.queues import ResponseQueue
from .utils.module_loading import import_module
import logging


class ChatBot(object):

    def __init__(self, name, **kwargs):
        self.name = name
        kwargs['name'] = name

        storage_adapter = kwargs.get('storage_adapter',
            'chatterbot.adapters.storage.JsonFileStorageAdapter'
        )

        logic_adapters = kwargs.get('logic_adapters', [
            'chatterbot.adapters.logic.ClosestMatchAdapter'
        ])

        input_adapter = kwargs.get('input_adapter',
            'chatterbot.adapters.input.VariableInputTypeAdapter'
        )

        output_adapter = kwargs.get('output_adapter',
            'chatterbot.adapters.output.OutputFormatAdapter'
        )

        # The last 10 statement inputs and outputs
        self.recent_statements = ResponseQueue(maxsize=10)

        # The storage adapter must be an instance of StorageAdapter
        self.validate_adapter_class(storage_adapter, StorageAdapter)

        # The input adapter must be an instance of InputAdapter
        self.validate_adapter_class(input_adapter, InputAdapter)

        # The output adapter must be an instance of OutputAdapter
        self.validate_adapter_class(output_adapter, OutputAdapter)

        StorageAdapterClass = import_module(storage_adapter)
        InputAdapterClass = import_module(input_adapter)
        OutputAdapterClass = import_module(output_adapter)

        self.storage = StorageAdapterClass(**kwargs)
        self.logic = MultiLogicAdapter(**kwargs)
        self.input = InputAdapterClass(**kwargs)
        self.output = OutputAdapterClass(**kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = (import_module(F)() for F in filters)

        # Add required system logic adapter
        self.add_adapter('chatterbot.adapters.logic.NoKnowledgeAdapter')

        for adapter in logic_adapters:
            self.add_adapter(adapter, **kwargs)

        # Share context information such as the name, the current conversation,
        # or access to other adapters with each of the adapters
        self.storage.set_context(self)
        self.logic.set_context(self)
        self.input.set_context(self)
        self.output.set_context(self)

        # Use specified trainer or fall back to the default
        trainer = kwargs.get('trainer', 'chatterbot.trainers.Trainer')
        TrainerClass = import_module(trainer)
        self.trainer = TrainerClass(self.storage)

        self.logger = kwargs.get('logger', logging.getLogger(__name__))

    def add_adapter(self, adapter, **kwargs):
        self.validate_adapter_class(adapter, LogicAdapter)

        NewAdapter = import_module(adapter)
        adapter = NewAdapter(**kwargs)
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
                del(self.logic.adapters[index])
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

    def get_last_conversance(self):
        """
        Return the most recent input statement and response pair.
        """
        if not self.recent_statements.empty():
            return self.recent_statements[-1]
        return None

    def get_last_response_statement(self):
        """
        Return the last statement that was received.
        """
        previous_interaction = self.get_last_conversance()
        if previous_interaction:
            # Return the output statement
            return previous_interaction[1]
        return None

    def get_last_input_statement(self):
        """
        Return the last response that was given.
        """
        previous_interaction = self.get_last_conversance()
        if previous_interaction:
            # Return the input statement
            return previous_interaction[0]
        return None

    def get_response(self, input_item):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :returns: A response to the input.
        :rtype: Statement
        """
        input_statement = self.input.process_input_statement(input_item)

        statement, response, confidence = self.generate_response(input_statement)

        # Learn that the user's input was a valid response to the chat bot's previous output
        self.learn_response(statement)

        self.recent_statements.append(
            (statement, response, )
        )

        # Process the response output with the output adapter
        return self.output.process_response(response, confidence)

    def generate_response(self, input_statement):
        """
        Return a response based on a given input statement.
        """
        self.storage.generate_base_query(self)

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)
        self.logger.info(u'Selecting "{}" as response with a confidence of {}'.format(response.text, confidence))

        return input_statement, response, confidence

    def learn_response(self, statement):
        """
        Learn that the statement provided is a valid response.
        """
        previous_statement = self.get_last_response_statement()

        if previous_statement:
            statement.add_response(
                Response(previous_statement.text)
            )
            self.logger.info(u'Adding "{}" as a response to "{}"'.format(
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
    def from_config(self, config_file_path):
        import json
        with open(config_file_path, 'r') as config_file:
            data = json.load(config_file)

        name = data.pop('name')

        return ChatBot(name, **data)

    class InvalidAdapterException(Exception):

        def __init__(self, value='Recieved an unexpected adapter setting.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
