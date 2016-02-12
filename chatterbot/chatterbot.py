from .adapters.exceptions import UnknownAdapterTypeException
from .adapters.storage import StorageAdapter
from .adapters.logic import LogicAdapter, MultiLogicAdapter
from .adapters.io import IOAdapter, MultiIOAdapter
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

        io_adapter = kwargs.get("io_adapter",
            "chatterbot.adapters.io.TerminalAdapter"
        )

        io_adapters = kwargs.get("io_adapters", [
            io_adapter
        ])

        self.recent_statements = []
        self.storage_adapters = []

        self.logic = MultiLogicAdapter(**kwargs)
        self.io = MultiIOAdapter(**kwargs)

        # Add required system adapter
        self.add_adapter("chatterbot.adapters.logic.NoKnowledgeAdapter")

        self.add_adapter(storage_adapter, **kwargs)

        for adapter in io_adapters:
            self.add_adapter(adapter, **kwargs)

        for adapter in logic_adapters:
            self.add_adapter(adapter, **kwargs)

        # Share context information such as the name, the current conversation,
        # or access to other adapters with each of the adapters
        self.storage.set_context(self)
        self.logic.set_context(self)
        self.io.set_context(self)

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
        elif issubclass(NewAdapter, IOAdapter):
            self.io.add_adapter(adapter)
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
        return self.io.process_input()

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
        return self.io.process_response(response)

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
