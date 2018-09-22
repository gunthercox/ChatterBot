import logging
from .storage import StorageAdapter
from .logic import LogicAdapter
from .input import InputAdapter
from .output import OutputAdapter
from . import utils


class ChatBot(object):
    """
    A conversational dialog chat bot.
    """

    def __init__(self, name, **kwargs):
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

        # Logic adapters used by the chat bot
        self.logic_adapters = []

        # Required logic adapters that must always be present
        self.system_logic_adapters = []

        self.storage = utils.initialize_class(storage_adapter, **kwargs)
        self.input = utils.initialize_class(input_adapter, **kwargs)
        self.output = utils.initialize_class(output_adapter, **kwargs)

        filters = kwargs.get('filters', tuple())
        self.filters = tuple([utils.import_module(F)() for F in filters])

        # Add required system logic adapter
        for system_logic_adapter in system_logic_adapters:
            utils.validate_adapter_class(system_logic_adapter, LogicAdapter)
            logic_adapter = utils.initialize_class(system_logic_adapter, **kwargs)
            logic_adapter.set_chatbot(self)
            self.system_logic_adapters.append(logic_adapter)

        for adapter in logic_adapters:
            utils.validate_adapter_class(adapter, LogicAdapter)
            logic_adapter = utils.initialize_class(adapter, **kwargs)
            logic_adapter.set_chatbot(self)
            self.logic_adapters.append(logic_adapter)

        # Add the chatbot instance to each adapter to share information such as
        # the name, the current conversation, or other adapters
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

        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        # Allow the bot to save input it receives so that it can learn
        self.read_only = kwargs.get('read_only', False)

        if kwargs.get('initialize', True):
            self.initialize()

    def initialize(self):
        """
        Do any work that needs to be done before the responses can be returned.
        """
        for logic_adapter in self.get_logic_adapters():
            logic_adapter.initialize()

    def get_response(self, input_item):
        """
        Return the bot's response based on the input.

        :param input_item: An input value.
        :returns: A response to the input.
        :rtype: Statement
        """
        input_statement = self.input.process_input(input_item)

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(self, input_statement)

        response = self.generate_response(input_statement)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.get_latest_response(input_statement.conversation)

        if not self.read_only:
            self.learn_response(input_statement, previous_statement)

        # Process the response output with the output adapter
        return self.output.process_response(response)

    def generate_response(self, input_statement):
        """
        Return a response based on a given input statement.

        :param input_statement: The input statement to be processed.
        """
        from collections import Counter

        self.storage.generate_base_query(self, input_statement.conversation)

        results = []
        result = None
        max_confidence = -1

        for adapter in self.get_logic_adapters():
            if adapter.can_process(input_statement):

                output = adapter.process(input_statement)
                results.append((output.confidence, output, ))

                self.logger.info(
                    '{} selected "{}" as a response with a confidence of {}'.format(
                        adapter.class_name, output.text, output.confidence
                    )
                )

                if output.confidence > max_confidence:
                    result = output
                    max_confidence = output.confidence
            else:
                self.logger.info(
                    'Not processing the statement using {}'.format(adapter.class_name)
                )

        # If multiple adapters agree on the same statement,
        # then that statement is more likely to be the correct response
        if len(results) >= 3:
            statements = [s[1] for s in results]
            count = Counter(statements)
            most_common = count.most_common()
            if most_common[0][1] > 1:
                result = most_common[0][0]
                max_confidence = utils.get_greatest_confidence(result, results)

        result.confidence = max_confidence
        result.conversation = input_statement.conversation

        return result

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
            tags=statement.tags
        )

    def get_latest_response(self, conversation):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
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

    def get_logic_adapters(self):
        """
        Return a list of all logic adapters being used, including system logic adapters.
        """
        adapters = []
        adapters.extend(self.logic_adapters)
        adapters.extend(self.system_logic_adapters)
        return adapters
