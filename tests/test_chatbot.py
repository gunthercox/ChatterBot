from tests.base_case import ChatBotTestCase
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class ChatterBotResponseTestCase(ChatBotTestCase):

    def setUp(self):
        super().setUp()

        self.test_statement = Statement(text='Hello', in_response_to='Hi')

    def test_get_initialization_functions(self):
        """
        Test that the initialization functions are returned.
        """
        functions = self.chatbot.get_initialization_functions()

        self.assertIn('initialize_nltk_stopwords', functions)
        self.assertIsLength(functions, 1)

    def test_get_initialization_functions_synset_distance(self):
        """
        Test that the initialization functions are returned.
        """
        from chatterbot.comparisons import synset_distance

        self.chatbot.logic_adapters[0].compare_statements = synset_distance
        functions = self.chatbot.get_initialization_functions()

        self.assertIn('initialize_nltk_stopwords', functions)
        self.assertIn('initialize_nltk_wordnet', functions)
        self.assertIn('initialize_nltk_punkt', functions)
        self.assertIsLength(functions, 3)

    def test_get_initialization_functions_sentiment_comparison(self):
        """
        Test that the initialization functions are returned.
        """
        from chatterbot.comparisons import sentiment_comparison

        self.chatbot.logic_adapters[0].compare_statements = sentiment_comparison
        functions = self.chatbot.get_initialization_functions()

        self.assertIn('initialize_nltk_stopwords', functions)
        self.assertIn('initialize_nltk_vader_lexicon', functions)
        self.assertIsLength(functions, 2)

    def test_get_initialization_functions_jaccard_similarity(self):
        """
        Test that the initialization functions are returned.
        """
        from chatterbot.comparisons import jaccard_similarity

        self.chatbot.logic_adapters[0].compare_statements = jaccard_similarity
        functions = self.chatbot.get_initialization_functions()

        self.assertIn('initialize_nltk_wordnet', functions)
        self.assertIn('initialize_nltk_stopwords', functions)
        self.assertIn('initialize_nltk_averaged_perceptron_tagger', functions)
        self.assertIsLength(functions, 3)

    def test_empty_database(self):
        """
        If there is no statements in the database, then the
        user's input is the only thing that can be returned.
        """
        response = self.chatbot.get_response('How are you?')

        self.assertEqual('How are you?', response)

    def test_statement_saved_empty_database(self):
        """
        Test that when database is empty, the first
        statement is saved and returned as a response.
        """
        statement_text = 'Wow!'
        response = self.chatbot.get_response(statement_text)

        results = list(self.chatbot.storage.filter(text=statement_text))

        self.assertIsLength(results, 1)
        self.assertEqual(response, statement_text)

    def test_statement_added_to_conversation(self):
        """
        An input statement should be added to the recent response list.
        """
        statement = Statement(text='Wow!', conversation='test')
        response = self.chatbot.get_response(statement)

        self.assertEqual(statement.text, response)
        self.assertEqual(response.conversation, 'test')

    def test_response_known(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')

        self.assertEqual(response, self.test_statement.text)

    def test_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')
        results = list(self.chatbot.storage.filter(text=response.text))

        self.assertEqual(response, self.test_statement.text)
        self.assertIsLength(results, 1)
        self.assertEqual(results[0].in_response_to, 'Hi')

    def test_second_response_format(self):
        self.chatbot.storage.update(self.test_statement)

        response = self.chatbot.get_response('Hi')
        self.assertEqual(response.text, 'Hello')

        second_response = self.chatbot.get_response('How are you?')
        results = list(self.chatbot.storage.filter(text=second_response.text))

        # Make sure that the second response was saved to the database
        self.assertIsLength(list(self.chatbot.storage.filter(text='How are you?')), 1)

        self.assertEqual(second_response, self.test_statement.text)
        self.assertIsLength(results, 1)
        self.assertEqual(results[0].in_response_to, 'Hi')

    def test_get_response_unicode(self):
        """
        Test the case that a unicode string is passed in.
        """
        response = self.chatbot.get_response(u'سلام')
        self.assertGreater(len(response.text), 0)

    def test_get_response_emoji(self):
        """
        Test the case that the input string contains an emoji.
        """
        response = self.chatbot.get_response(u'💩 ')
        self.assertGreater(len(response.text), 0)

    def test_get_response_non_whitespace(self):
        """
        Test the case that a non-whitespace C1 control string is passed in.
        """
        response = self.chatbot.get_response(u'')
        self.assertGreater(len(response.text), 0)

    def test_get_response_two_byte_characters(self):
        """
        Test the case that a string containing two-byte characters is passed in.
        """
        response = self.chatbot.get_response(u'田中さんにあげて下さい')
        self.assertGreater(len(response.text), 0)

    def test_get_response_corrupted_text(self):
        """
        Test the case that a string contains "corrupted" text.
        """
        response = self.chatbot.get_response(u'Ṱ̺̺̕h̼͓̲̦̳̘̲e͇̣̰̦̬͎ ̢̼̻̱̘h͚͎͙̜̣̲ͅi̦̲̣̰̤v̻͍e̺̭̳̪̰-m̢iͅn̖̺̞̲̯̰d̵̼̟͙̩̼̘̳.̨̹͈̣')
        self.assertGreater(len(response.text), 0)

    def test_response_with_tags_added(self):
        """
        If an input statement has tags added to it,
        that data should saved with the input statement.
        """
        self.test_statement.add_tags('test')
        self.chatbot.get_response(
            self.test_statement
        )

        results = list(self.chatbot.storage.filter(text=self.test_statement.text))

        self.assertIsLength(results, 1)
        self.assertIn('test', results[0].get_tags())

    def test_get_response_with_text_and_kwargs(self):
        self.chatbot.get_response('Hello', conversation='greetings')

        results = list(self.chatbot.storage.filter(text='Hello'))

        self.assertIsLength(results, 1)
        self.assertEqual(results[0].conversation, 'greetings')

    def test_get_response_missing_text(self):
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response()

    def test_get_response_missing_text_with_conversation(self):
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response(conversation='test')

    def test_generate_response(self):
        statement = Statement(text='Many insects adopt a tripedal gait for rapid yet stable walking.')
        response = self.chatbot.generate_response(statement)

        self.assertEqual(response, statement)
        self.assertEqual(response.confidence, 1)

    def test_learn_response(self):
        previous_response = Statement(text='Define Hemoglobin.')
        statement = Statement(text='Hemoglobin is an oxygen-transport metalloprotein.')
        self.chatbot.learn_response(statement, previous_response)
        results = list(self.chatbot.storage.filter(text=statement.text))

        self.assertIsLength(results, 1)

    def test_get_response_does_not_add_new_statement(self):
        """
        Test that a new statement is not learned if `read_only` is set to True.
        """
        self.chatbot.read_only = True
        self.chatbot.get_response('Hi!')
        results = list(self.chatbot.storage.filter(text='Hi!'))

        self.assertIsLength(results, 0)

    def test_get_latest_response_from_zero_responses(self):
        response = self.chatbot.get_latest_response('invalid')

        self.assertIsNone(response)

    def test_get_latest_response_from_one_responses(self):
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')

        response = self.chatbot.get_latest_response('test')

        self.assertEqual(response.text, 'A')

    def test_get_latest_response_from_two_responses(self):
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')
        self.chatbot.storage.create(text='C', conversation='test', in_response_to='B')

        response = self.chatbot.get_latest_response('test')

        self.assertEqual(response.text, 'B')

    def test_get_latest_response_from_three_responses(self):
        self.chatbot.storage.create(text='A', conversation='test')
        self.chatbot.storage.create(text='B', conversation='test', in_response_to='A')
        self.chatbot.storage.create(text='C', conversation='test', in_response_to='B')
        self.chatbot.storage.create(text='D', conversation='test', in_response_to='C')

        response = self.chatbot.get_latest_response('test')

        self.assertEqual(response.text, 'C')

    def test_search_text_results_after_training(self):
        """
        ChatterBot should return close matches to an input
        string when filtering using the search_text parameter.
        """
        self.chatbot.storage.create_many([
            Statement('Example A for search.'),
            Statement('Another example.'),
            Statement('Example B for search.'),
            Statement(text='Another statement.'),
        ])

        results = list(self.chatbot.storage.filter(
            search_text=self.chatbot.storage.stemmer.get_bigram_pair_string(
                'Example A for search.'
            )
        ))

        self.assertEqual('Example A for search.', results[0].text)
        self.assertEqual('Example B for search.', results[1].text)
        self.assertIsLength(results, 2)


class TestAdapterA(LogicAdapter):

    def process(self, statement):
        response = Statement(text='Good morning.')
        response.confidence = 0.2
        return response


class TestAdapterB(LogicAdapter):

    def process(self, statement):
        response = Statement(text='Good morning.')
        response.confidence = 0.5
        return response


class TestAdapterC(LogicAdapter):

    def process(self, statement):
        response = Statement(text='Good night.')
        response.confidence = 0.7
        return response


class ChatBotLogicAdapterTestCase(ChatBotTestCase):

    def test_sub_adapter_agreement(self):
        """
        In the case that multiple adapters agree on a given
        statement, this statement should be returned with the
        highest confidence available from these matching options.
        """
        self.chatbot.logic_adapters = [
            TestAdapterA(self.chatbot),
            TestAdapterB(self.chatbot),
            TestAdapterC(self.chatbot)
        ]

        statement = self.chatbot.generate_response(Statement(text='Howdy!'))

        self.assertEqual(statement.confidence, 0.5)
        self.assertEqual(statement, 'Good morning.')

    def test_get_logic_adapters(self):
        """
        Test that all system logic adapters and regular logic adapters
        can be retrieved as a list by a single method.
        """
        adapter_a = TestAdapterA(self.chatbot)
        adapter_b = TestAdapterB(self.chatbot)
        self.chatbot.system_logic_adapters = [adapter_a]
        self.chatbot.logic_adapters = [adapter_b]

        self.assertIsLength(self.chatbot.get_logic_adapters(), 2)
        self.assertIn(adapter_a, self.chatbot.get_logic_adapters())
        self.assertIn(adapter_b, self.chatbot.get_logic_adapters())

    def test_chatbot_set_for_all_logic_adapters(self):
        for sub_adapter in self.chatbot.get_logic_adapters():
            self.assertEqual(sub_adapter.chatbot, self.chatbot)
        self.assertGreater(
            len(self.chatbot.get_logic_adapters()), 0,
            msg='At least one logic adapter is expected for this test.'
        )

    def test_response_persona_is_bot(self):
        """
        The response returned from the chatbot should be set to the name of the chatbot.
        """
        response = self.chatbot.get_response('Hey everyone!')

        self.assertEqual(response.persona, 'bot:Test Bot')
