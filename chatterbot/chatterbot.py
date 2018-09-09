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
        self.trainer = TrainerClass(self, **kwargs)
        self.training_data = kwargs.get('training_data')

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

    def get_response(self, input_item, conversation='default'):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :param conversation: A string of characters unique to the conversation.
        :returns: A response to the input.
        :rtype: Statement
        """
        input_statement = self.input.process_input(
            input_item,
            conversation
        )

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        response = self.generate_response(input_statement)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.get_latest_response(input_statement.conversation)

        if not self.read_only:
            self.learn_response(input_statement, previous_statement)

        # Process the response output with the output adapter
        return self.output.process_response(response, conversation)

    def generate_response(self, input_statement):
        """
        Return a response based on a given input statement.
        """
        self.storage.generate_base_query(self, input_statement.conversation)

        # Select a response to the input statement
        response = self.logic.process(input_statement)

        return response

    def learn_response(self, statement, previous_statement):
        """
        Learn that the statement provided is a valid response.
        """
        previous_statement_text = previous_statement

        if previous_statement is not None:
            previous_statement_text = previous_statement.text

        self.logger.info('Adding "{}" as a response to "{}"'.format(
            statement.text,
            previous_statement_text
        ))

        # Save the statement after selecting a response
        self.storage.create(
            text=statement.text,
            in_response_to=previous_statement_text,
            conversation=statement.conversation,
            extra_data=statement.extra_data,
            tags=statement.tags
        )

    def get_latest_response(self, conversation):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.

        # TODO: Write tests for this method.
        """
        from .conversation import Statement as StatementObject

        conversation_statements = self.storage.filter(
            conversation=conversation,
            order_by=['id']
        )

        # Get the most recent statement in the conversation if one exists
        latest_statement = conversation_statements[-1] if conversation_statements else None

        if latest_statement:
            if latest_statement.in_response_to:

                response_statements = self.storage.filter(
                    conversation=conversation,
                    text=latest_statement.in_response_to,
                    order_by=['id']
                )

                if response_statements:
                    return response_statements[-1]
                else:
                    return StatementObject(
                        text=latest_statement.in_response_to,
                        conversation=conversation
                    )
            else:
                # The case that the latest statement is not in response to another statement
                return latest_statement

        return None

    def set_trainer(self, training_class, **kwargs):
        """
        Set the module used to train the chatbot.

        :param training_class: The training class to use for the chat bot.
        :type training_class: `Trainer`

        :param \**kwargs: Any parameters that should be passed to the training class.
        """
        self.trainer = training_class(self, **kwargs)

    @property
    def train(self):
        """
        Proxy method to the chat bot's trainer class.
        """
        return self.trainer.train
