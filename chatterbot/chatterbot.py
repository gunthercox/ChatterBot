from .adapters.exceptions import UnknownAdapterTypeException
from .adapters.storage import StorageAdapter
from .adapters.logic import LogicAdapter, MultiLogicAdapter
from .adapters.input import InputAdapter, MultiInputAdapter
from .adapters.output import OutputAdapter, MultiOutputAdapter
from .utils.module_loading import import_module
from .conversation import Statement


class ChatBot(object):

    def __init__(self, name, **kwargs):
        kwargs["name"] = name

        storage_adapter = kwargs.get("storage_adapter",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )

        logic_adapter = kwargs.get("logic_adapter",
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )

        logic_adapters = kwargs.get("logic_adapters", [
            logic_adapter
        ])

        input_output_adapter_pairs = kwargs.get("io_adapter_pairs",
            (
                "chatterbot.adapters.input.TerminalAdapter",
                "chatterbot.adapters.output.TerminalAdapter",
            ),
        )

        self.recent_statements = []
        self.storage_adapters = []

        self.logic = MultiLogicAdapter(**kwargs)
        self.input = MultiInputAdapter(**kwargs)
        self.output = MultiOutputAdapter(**kwargs)

        # Add required system adapter
        self.add_adapter("chatterbot.adapters.logic.NoKnowledgeAdapter")

        self.add_adapter(storage_adapter, **kwargs)

        for adapter_pair in input_output_adapter_pairs:

            # Validate the input output adapter tuples

            if len(adapter_pair) != 2:
                raise self.InvalidAdapterPairException(
                    'Expected list of tuples with each tuple a length of 2.'
                )

            input_adapter = adapter_pair[0]
            output_adapter = adapter_pair[1]

            # The first adapter must be an instance of an input adapter
            if not issubclass(import_module(input_adapter), InputAdapter):
                raise self.InvalidAdapterPairException(
                    '{} is not an input adapter'.format(input_adapter)
                )

            # The second adapter must be an instance of an output adapter
            if not issubclass(import_module(output_adapter), OutputAdapter):
                raise self.InvalidAdapterPairException(
                    '{} is not an output adapter'.format(output_adapter)
                )

            self.add_adapter(input_adapter, **kwargs)
            self.add_adapter(output_adapter, **kwargs)

        for adapter in logic_adapters:
            self.add_adapter(adapter, **kwargs)

        # Share context information such as the name, the current conversation,
        # or access to other adapters with each of the adapters
        self.storage.set_context(self)
        self.logic.set_context(self)
        self.input.set_context(self)
        self.output.set_context(self)

    @property
    def storage(self):
        return self.storage_adapters[0]

    def add_adapter(self, adapter, **kwargs):
        NewAdapter = import_module(adapter)

        adapter = NewAdapter(**kwargs)

        if issubclass(NewAdapter, StorageAdapter):
            self.storage_adapters.append(adapter)
        elif issubclass(NewAdapter, LogicAdapter):
            self.logic.add_adapter(adapter)
        elif issubclass(NewAdapter, InputAdapter):
            self.input.add_adapter(adapter)
        elif issubclass(NewAdapter, OutputAdapter):
            self.output.add_adapter(adapter)
        else:
            raise UnknownAdapterTypeException()

    def get_last_statement(self):
        """
        Return the last statement that was received.
        """
        if self.recent_statements:
            return self.recent_statements[-1]
        return None

    def get_input(self):
        return self.input.process_input()

    def get_response(self, input_text):
        """
        Return the bot's response based on the input.
        """
        input_statement = Statement(input_text)

        # Select a response to the input statement
        confidence, response = self.logic.process(input_statement)

        existing_statement = self.storage.find(input_statement.text)

        if existing_statement:
            input_statement = existing_statement

        previous_statement = self.get_last_statement()

        if previous_statement:
            input_statement.add_response(previous_statement)

        # Update the database after selecting a response
        self.storage.update(input_statement)

        self.recent_statements.append(response)

        # Process the response output with the IO adapter
        return self.output.process_response(response)

    def train(self, conversation=None, *args, **kwargs):
        """
        Train the chatbot based on input data.
        """
        from .training import Trainer

        trainer = Trainer(self.storage)

        if isinstance(conversation, str):
            corpora = list(args)
            corpora.append(conversation)

            if corpora:
                trainer.train_from_corpora(corpora)
        else:
            trainer.train_from_list(conversation)

    class InvalidAdapterPairException(Exception):
        def __init__(self, message='Recieved an unexpected pair of adapters.'):
            super(ChatBot.InvalidAdapterPairException, self).__init__(message)

        def __str__(self):
            return self.message
