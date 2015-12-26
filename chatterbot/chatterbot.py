from .adapters import Adaptation
from .conversation import Statement, Response
from .utils.module_loading import import_module


class ChatBot(Adaptation):

    def __init__(self, name, **kwargs):
        super(ChatBot, self).__init__(**kwargs)

        self.context.name = name
        self.context.recent_statements = []

        storage_adapter = kwargs.get("storage_adapter",
            "chatterbot.adapters.storage.JsonDatabaseAdapter"
        )

        logic_adapter = kwargs.get("logic_adapter",
            "chatterbot.adapters.logic.ClosestMatchAdapter"
        )

        io_adapter = kwargs.get("io_adapter",
            "chatterbot.adapters.io.TerminalAdapter"
        )

        PluginChooser = import_module("chatterbot.adapters.plugins.PluginChooser")
        self.plugin_chooser = PluginChooser(**kwargs)

        self.storage = self.add_adapter('storage', storage_adapter)
        self.logic = self.add_adapter('logic', logic_adapter)
        self.io = self.add_adapter('io', io_adapter)

        self.trainer = None

    def get_last_statement(self):
        """
        Return the last statement that was received.
        """
        if self.context.recent_statements:
            return self.context.recent_statements[-1]
        return None

    def get_response(self, input_text):
        """
        Return the bot's response based on the input.
        """
        input_statement = Statement(input_text)

        # Applying plugin logic to see whether the chatbot should respond in this way
        plugin_response = self.plugin_chooser.choose(input_statement)

        if not plugin_response is False:
            return self.io.process_response(Statement(plugin_response))

        # If no responses exist, return the input statement
        if not self.storage.count():
            self.storage.update(input_statement)
            self.context.recent_statements.append(input_statement)

            # Process the response output with the IO adapter
            return self.io.process_response(input_statement)

        # Select a response to the input statement
        response = self.logic.process(input_statement)

        existing_statement = self.storage.find(input_statement.text)

        if existing_statement:
            input_statement = existing_statement

        previous_statement = self.get_last_statement()

        if previous_statement:
            input_statement.add_response(previous_statement)

        # Update the database after selecting a response
        self.storage.update(input_statement)

        self.context.recent_statements.append(response)

        # Process the response output with the IO adapter
        return self.io.process_response(response)

    def get_input(self):
        return self.io.process_input()

    def train(self, conversation=None, *args, **kwargs):
        """
        Train the chatbot based on input data.
        """
        from .training import Trainer

        self.trainer = Trainer(self.storage)

        if isinstance(conversation, str):
            corpora = list(args)
            corpora.append(conversation)

            if corpora:
                self.trainer.train_from_corpora(corpora)
        else:
            self.trainer.train_from_list(conversation)

