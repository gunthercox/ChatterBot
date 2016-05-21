from .adapters.storage import StorageAdapter
from .adapters.logic import LogicAdapter, MultiLogicAdapter
from .adapters.input import InputAdapter
from .adapters.output import OutputAdapter
from .conversation import Statement
from .utils.queues import ResponseQueue
from .utils.module_loading import import_module


class ChatBot(object):

    def __init__(self, name, **kwargs):
        kwargs["name"] = name

        storage_adapter = kwargs.get("storage_adapter",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )

        logic_adapters = kwargs.get("logic_adapters", [
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        ])

        input_adapter = kwargs.get("input_adapter",
            "chatterbot.adapters.input.VariableInputTypeAdapter"
        )

        output_adapter = kwargs.get("output_adapter",
            "chatterbot.adapters.output.OutputFormatAdapter"
        )

        input_output_adapter_pairs = kwargs.get(
            "io_adapter_pairs"
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

        # Add required system logic adapter
        self.add_adapter("chatterbot.adapters.logic.NoKnowledgeAdapter")

        for adapter in logic_adapters:
            self.add_adapter(adapter, **kwargs)

        # Share context information such as the name, the current conversation,
        # or access to other adapters with each of the adapters
        self.storage.set_context(self)
        self.logic.set_context(self)
        self.input.set_context(self)
        self.output.set_context(self)

        self.trainer = None

    def add_adapter(self, adapter, **kwargs):
        self.validate_adapter_class(adapter, LogicAdapter)

        NewAdapter = import_module(adapter)
        adapter = NewAdapter(**kwargs)
        self.logic.add_adapter(adapter)

    def validate_adapter_class(self, validate_class, adapter_class):
        """
        Raises an exception if validate_class is
        not a subclass of adapter_class.
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
        """
        input_statement = self.input.process_input(input_item)

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)

        existing_statement = self.storage.find(input_statement.text)

        if existing_statement:
            input_statement = existing_statement

        previous_statement = self.get_last_response_statement()

        if previous_statement:
            input_statement.add_response(previous_statement)

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
        if not self.trainer:
            raise self.TrainerInitializationException()
        # Proxy method to the trainer
        return self.trainer.train

    class InvalidAdapterException(Exception):

        def __init__(self, message='Recieved an unexpected adapter setting.'):
            super(ChatBot.InvalidAdapterException, self).__init__(message)

        def __str__(self):
            return self.message

    class TrainerInitializationException(Exception):

        def __init__(self, message='The `set_trainer` method must be called before calling `train`.'):
            super(ChatBot.TrainerInitializationException, self).__init__(message)

        def __str__(self):
            return self.message
