import logging
from chatterbot.storage import StorageAdapter
from chatterbot.logic import LogicAdapter
from chatterbot.search import IndexedTextSearch
from chatterbot.conversation import Statement
from chatterbot import utils


class ChatBot(object):
    """
    A conversational dialog chat bot.
    """

    def __init__(self, name, **kwargs):
        self.name = name

        primary_search_algorithm = IndexedTextSearch(self, **kwargs)

        self.search_algorithms = {
            primary_search_algorithm.name: primary_search_algorithm
        }

        storage_adapter = kwargs.get('storage_adapter', 'chatterbot.storage.SQLStorageAdapter')

        logic_adapters = kwargs.get('logic_adapters', [
            'chatterbot.logic.BestMatch'
        ])

        if 'input_adapter' in kwargs:
            raise Exception('input adapter')

        if 'output_adapter' in kwargs:
            raise Exception('output adapter')

        # Check that each adapter is a valid subclass of it's respective parent
        utils.validate_adapter_class(storage_adapter, StorageAdapter)

        # Logic adapters used by the chat bot
        self.logic_adapters = []

        self.storage = utils.initialize_class(storage_adapter, **kwargs)

        for adapter in logic_adapters:
            utils.validate_adapter_class(adapter, LogicAdapter)
            logic_adapter = utils.initialize_class(adapter, self, **kwargs)
            self.logic_adapters.append(logic_adapter)

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

    def get_initialization_functions(self):
        initialization_functions = utils.get_initialization_functions(
            self, 'storage.tagger'
        )

        for search_algorithm in self.search_algorithms.values():
            search_algorithm_functions = utils.get_initialization_functions(
                search_algorithm, 'compare_statements'
            )
            initialization_functions.update(search_algorithm_functions)

        return initialization_functions

    def initialize(self):
        """
        Do any work that needs to be done before the chatbot can process responses.
        """
        for function in self.get_initialization_functions().values():
            function()

    def get_response(self, statement=None, **kwargs):
        """
        Return the bot's response based on the input.

        :param statement: An statement object or string.
        :returns: A response to the input.
        :rtype: Statement
        """
        additional_response_selection_parameters = kwargs.pop('additional_response_selection_parameters', {})

        if isinstance(statement, str):
            kwargs['text'] = statement

        if statement is None and 'text' not in kwargs:
            raise self.ChatBotException(
                'Either a statement object or a "text" keyword '
                'argument is required. Neither was provided.'
            )

        if hasattr(statement, 'text'):
            data = statement.serialize()
            data.update(kwargs)
            kwargs = data

        if isinstance(statement, dict):
            statement.update(kwargs)
            kwargs = statement

        input_statement = Statement(**kwargs)

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(input_statement)

        response = self.generate_response(input_statement, additional_response_selection_parameters)

        # Learn that the user's input was a valid response to the chat bot's previous output
        previous_statement = self.get_latest_response(input_statement.conversation)

        if not self.read_only:
            self.learn_response(input_statement, previous_statement)

            # Save the response generated for the input
            self.storage.create(
                text=response.text,
                in_response_to=response.in_response_to,
                conversation=response.conversation,
                persona=response.persona
            )

        return response

    def generate_response(self, input_statement, additional_response_selection_parameters=None):
        """
        Return a response based on a given input statement.

        :param input_statement: The input statement to be processed.
        """
        from collections import Counter

        results = []
        result = None
        max_confidence = -1

        for adapter in self.logic_adapters:
            if adapter.can_process(input_statement):

                output = adapter.process(input_statement, additional_response_selection_parameters)
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
            statements = tuple(
                s[1] for s in results
            )
            count = Counter(statements)
            most_common = count.most_common()
            if most_common[0][1] > 1:
                result = most_common[0][0]
                max_confidence = utils.get_greatest_confidence(result, results)

        response = Statement(
            text=result.text,
            in_response_to=input_statement.text,
            conversation=input_statement.conversation,
            persona='bot:' + self.name
        )

        response.confidence = max_confidence

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

        # Save the input statement
        return self.storage.create(
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
        from chatterbot.conversation import Statement as StatementObject

        conversation_statements = list(self.storage.filter(
            conversation=conversation,
            order_by=['id']
        ))

        # Get the most recent statement in the conversation if one exists
        latest_statement = conversation_statements[-1] if conversation_statements else None

        if latest_statement:
            if latest_statement.in_response_to:

                response_statements = list(self.storage.filter(
                    conversation=conversation,
                    text=latest_statement.in_response_to,
                    order_by=['id']
                ))

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

    class ChatBotException(Exception):
        pass
