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

        default_storage = {"adapter_class": 'chatterbot.adapters.storage.JsonFileStorageAdapter'}
        storage_kwargs = kwargs.get('storage_adapter', default_storage)
        storage_adapter = storage_kwargs.get('adapter_class')
        database = storage_kwargs.get('database')

        default_logic = [{"adapter_class": 'chatterbot.adapters.logic.ClosestMatchAdapter'}]
        logic_kwargs = kwargs.get('logic_adapters', default_logic)
        logic_adapters = [dic['adapter_class'] for dic in logic_kwargs]

        default_input = {"adapter_class": 'chatterbot.adapters.input.VariableInputTypeAdapter'}
        input_kwargs = kwargs.get('input_adapter', default_input)
        input_adapter = input_kwargs.get('adapter_class')

        default_output = {"adapter_class": 'chatterbot.adapters.output.OutputFormatAdapter'}
        output_kwargs = kwargs.get('output_adapter', default_output)
        output_adapter = output_kwargs.get('adapter_class')

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

        self.storage = StorageAdapterClass(**storage_kwargs)
        mapping = {"output_adapter": output_adapter,
                    "input_adapter": input_adapter,
                    'name': name,
                    'database': database}
        self.logic = MultiLogicAdapter(**mapping)
        self.input = InputAdapterClass(**input_kwargs)
        self.output = OutputAdapterClass(**output_kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = (import_module(F)() for F in filters)

        # Add required system logic adapter
        self.add_adapter('chatterbot.adapters.logic.NoKnowledgeAdapter')

        for adapter in logic_adapters:
            self.add_adapter(adapter, **mapping)

        # Share context information such as the name, the current conversation,
        # or access to other adapters with each of the adapters
        self.storage.set_context(self)
        self.logic.set_context(self)
        self.input.set_context(self)
        self.output.set_context(self)

        # Use specified trainer or fall back to the default
        default_trainer = {'trainer_class': 'chatterbot.trainers.Trainer'}
        trainer_kwargs = kwargs.get('trainer', default_trainer)
        trainer = trainer_kwargs.get('trainer_class')
        TrainerClass = import_module(trainer)
        self.trainer = TrainerClass(self.storage)

        self.logger = kwargs.get('logger', logging.getLogger(__name__))

    def add_adapter(self, adapter, **kwargs):
        self.validate_adapter_class(adapter, LogicAdapter)

        NewAdapter = import_module(adapter)
        adapter = NewAdapter(**kwargs)
        self.logic.add_adapter(adapter)

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
        :returns: Statement -- the response to the input.
        """
        input_statement = self.input.process_input(input_item)
        self.logger.info(u'Recieved input statement: {}'.format(input_statement.text))

        self.storage.generate_base_query(self)

        existing_statement = self.storage.find(input_statement.text)

        if existing_statement:
            self.logger.info(u'"{}" is a known statement'.format(input_statement.text))
            if input_statement.extra_data:
                existing_statement.extra_data.update(input_statement.extra_data)
            input_statement = existing_statement
        else:
            self.logger.info(u'"{}" is not a known statement'.format(input_statement.text))

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)
        self.logger.info(u'Selecting "{}" as response with a confidence of {}'.format(response.text, confidence))

        if input_statement.extra_data:
            response.extra_data.update(input_statement.extra_data)

        previous_statement = self.get_last_response_statement()

        if previous_statement:
            input_statement.add_response(
                Response(previous_statement.text)
            )
            self.logger.info(u'Adding the previous statement "{}" as response to "{}"'.format(
                previous_statement.text,
                input_statement.text
            ))

        # Update the database after selecting a response
        self.storage.update(input_statement)

        self.recent_statements.append(
            (input_statement, response, )
        )

        # Process the response output with the output adapter
        return self.output.process_response(response)

    def set_trainer(self, training_class, **kwargs):
        """
        Set the module used to train the chatbot.
        """
        self.trainer = training_class(self.storage, **kwargs)

    @property
    def train(self):
        """
        Proxy method to the chat bot's trainer class.
        """
        return self.trainer.train

    class InvalidAdapterException(Exception):

        def __init__(self, value='Recieved an unexpected adapter setting.'):
            self.value = value

        def __str__(self):
            return repr(self.value)
