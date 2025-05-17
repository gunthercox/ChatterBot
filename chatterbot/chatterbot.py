import logging
from typing import Union
from chatterbot.storage import StorageAdapter
from chatterbot.logic import LogicAdapter
from chatterbot.search import TextSearch, IndexedTextSearch
from chatterbot.tagging import PosLemmaTagger
from chatterbot.conversation import Statement
from chatterbot import languages
from chatterbot import utils
import spacy


class ChatBot(object):
    """
    A conversational dialog chat bot.

    :param name: A name is the only required parameter for the ChatBot class.
    :type name: str

    :keyword storage_adapter: The dot-notated import path to a storage adapter class.
                              Defaults to ``"chatterbot.storage.SQLStorageAdapter"``.
    :type storage_adapter: str

    :param logic_adapters: A list of dot-notated import paths to each logic adapter the bot uses.
                           Defaults to ``["chatterbot.logic.BestMatch"]``.
    :type logic_adapters: list

    :param tagger: The tagger to use for the chat bot.
                   Defaults to :class:`~chatterbot.tagging.PosLemmaTagger`
    :type tagger: object

    :param tagger_language: The language to use for the tagger.
                            Defaults to :class:`~chatterbot.languages.ENG`.
    :type tagger_language: object

    :param preprocessors: A list of preprocessor functions to use for the chat bot.
    :type preprocessors: list

    :param read_only: If True, the chat bot will not save any input it receives, defaults to False.
    :type read_only: bool

    :param logger: A ``Logger`` object.
    :type logger: logging.Logger

    :param model: A definition used to load a large language model.
                  Defaults to ``None``.
                  (Added in version 1.2.7)
    :type model: dict

    :param stream: Return output as a streaming responses when a ``model`` is defined.
                   (Added in version 1.2.7)
    """

    def __init__(self, name, stream=False, **kwargs):
        self.name = name

        self.stream = stream

        self.logger = kwargs.get('logger', logging.getLogger(__name__))

        storage_adapter = kwargs.get('storage_adapter', 'chatterbot.storage.SQLStorageAdapter')

        logic_adapters = kwargs.get('logic_adapters', [
            'chatterbot.logic.BestMatch'
        ])

        # Check that each adapter is a valid subclass of it's respective parent
        utils.validate_adapter_class(storage_adapter, StorageAdapter)

        # Logic adapters used by the chat bot
        self.logic_adapters = []

        self.storage = utils.initialize_class(storage_adapter, **kwargs)

        tagger_language = kwargs.get('tagger_language', languages.ENG)

        try:
            Tagger = kwargs.get('tagger', PosLemmaTagger)

            self.tagger = Tagger(language=tagger_language)
        except IOError as io_error:
            # Return a more helpful error message if possible
            if "Can't find model" in str(io_error):
                model_name = utils.get_model_for_language(tagger_language)
                if hasattr(tagger_language, 'ENGLISH_NAME'):
                    language_name = tagger_language.ENGLISH_NAME
                else:
                    language_name = tagger_language
                raise self.ChatBotException(
                    'Setup error:\n'
                    f'The Spacy model for "{language_name}" language is missing.\n'
                    'Please install the model using the command:\n\n'
                    f'python -m spacy download {model_name}\n\n'
                    'See https://spacy.io/usage/models for more information about available models.'
                ) from io_error
            else:
                raise io_error

        primary_search_algorithm = IndexedTextSearch(self, **kwargs)
        text_search_algorithm = TextSearch(self, **kwargs)

        self.search_algorithms = {
            primary_search_algorithm.name: primary_search_algorithm,
            text_search_algorithm.name: text_search_algorithm
        }

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

        # NOTE: 'xx' is the language code for a multi-language model
        self.nlp = spacy.blank(self.tagger.language.ISO_639_1)

        self.model = None
        if model := kwargs.get('model'):
            import_path = model.pop('client')
            self.model = utils.initialize_class(import_path, self, **model)

        # Allow the bot to save input it receives so that it can learn
        self.read_only = kwargs.get('read_only', False)

    def get_response(self, statement: Union[Statement, str, dict] = None, **kwargs) -> Statement:
        """
        Return the bot's response based on the input.

        :param statement: An statement object or string.
        :returns: A response to the input.

        :param additional_response_selection_parameters: Parameters to pass to the
            chat bot's logic adapters to control response selection.
        :type additional_response_selection_parameters: dict

        :param persist_values_to_response: Values that should be saved to the response
            that the chat bot generates.
        :type persist_values_to_response: dict
        """
        Statement = self.storage.get_object('statement')

        additional_response_selection_parameters = kwargs.pop('additional_response_selection_parameters', {})

        persist_values_to_response = kwargs.pop('persist_values_to_response', {})

        if isinstance(statement, str):
            kwargs['text'] = statement

        if isinstance(statement, dict):
            kwargs.update(statement)

        if statement is None and 'text' not in kwargs:
            raise self.ChatBotException(
                'Either a statement object or a "text" keyword '
                'argument is required. Neither was provided.'
            )

        if hasattr(statement, 'serialize'):
            kwargs.update(**statement.serialize())

        tags = kwargs.pop('tags', [])

        text = kwargs.pop('text')

        input_statement = Statement(text=text, **kwargs)

        input_statement.add_tags(*tags)

        # Preprocess the input statement
        for preprocessor in self.preprocessors:
            input_statement = preprocessor(input_statement)

        # Mark the statement as being a response to the previous
        if input_statement.in_response_to is None:
            previous_statement = self.get_latest_response(input_statement.conversation)
            if previous_statement:
                input_statement.in_response_to = previous_statement.text

        # Make sure the input statement has its search text saved

        if not input_statement.search_text:
            _search_text = self.tagger.get_text_index_string(input_statement.text)
            input_statement.search_text = _search_text

        if not input_statement.search_in_response_to and input_statement.in_response_to:
            input_statement.search_in_response_to = self.tagger.get_text_index_string(
                input_statement.in_response_to
            )

        response = self.generate_response(
            input_statement,
            additional_response_selection_parameters
        )

        # If streaming is enabled return the response immediately
        if self.stream:
            return response

        # Update any response data that needs to be changed
        if persist_values_to_response:
            for response_key in persist_values_to_response:
                response_value = persist_values_to_response[response_key]
                if response_key == 'tags':
                    input_statement.add_tags(*response_value)
                    response.add_tags(*response_value)
                else:
                    setattr(input_statement, response_key, response_value)
                    setattr(response, response_key, response_value)

        if not self.read_only:

            # Save the input statement
            self.storage.create(**input_statement.serialize())

            # Save the response generated for the input
            self.learn_response(response, previous_statement=input_statement)


        return response

    def generate_response(self, input_statement, additional_response_selection_parameters=None):
        """
        Return a response based on a given input statement.

        :param input_statement: The input statement to be processed.
        """
        Statement = self.storage.get_object('statement')

        results = []
        result = None
        max_confidence = -1

        # If a model is provided, use it to process the input statement
        # instead of the logic adapters
        if self.model:
            model_response = self.model.process(input_statement)
            return model_response

        for adapter in self.logic_adapters:
            if adapter.can_process(input_statement):

                output = adapter.process(input_statement, additional_response_selection_parameters)
                results.append(output)

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

        class ResultOption:
            def __init__(self, statement, count=1):
                self.statement = statement
                self.count = count

        # If multiple adapters agree on the same statement,
        # then that statement is more likely to be the correct response
        if len(results) >= 3:
            result_options = {}
            for result_option in results:
                result_string = result_option.text + ':' + (result_option.in_response_to or '')

                if result_string in result_options:
                    result_options[result_string].count += 1
                    if result_options[result_string].statement.confidence < result_option.confidence:
                        result_options[result_string].statement = result_option
                else:
                    result_options[result_string] = ResultOption(
                        result_option
                    )

            most_common = list(result_options.values())[0]

            for result_option in result_options.values():
                if result_option.count > most_common.count:
                    most_common = result_option

            self.logger.info('Selecting "{}" as the most common response'.format(most_common.statement.text))

            if most_common.count > 1:
                result = most_common.statement

        response = Statement(
            text=result.text,
            in_response_to=input_statement.text,
            conversation=input_statement.conversation,
            persona='bot:' + self.name
        )

        response.add_tags(*result.get_tags())

        response.confidence = result.confidence

        return response

    def learn_response(self, statement, previous_statement=None):
        """
        Learn that the statement provided is a valid response.
        """
        if not previous_statement:
            previous_statement = statement.in_response_to

        if not previous_statement:
            previous_statement = self.get_latest_response(statement.conversation)
            if previous_statement:
                previous_statement = previous_statement.text

        previous_statement_text = previous_statement

        if not isinstance(previous_statement, (str, type(None), )):
            statement.in_response_to = previous_statement.text
        elif isinstance(previous_statement, str):
            statement.in_response_to = previous_statement

        self.logger.info('Adding "{}" as a response to "{}"'.format(
            previous_statement_text,
            statement.text
        ))

        if not statement.persona:
            statement.persona = 'bot:' + self.name

        # Save the response statement
        return self.storage.create(**statement.serialize())

    def get_latest_response(self, conversation: str):
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
        latest_statement = conversation_statements[-1] if len(conversation_statements) else None

        return latest_statement

    class ChatBotException(Exception):
        pass
