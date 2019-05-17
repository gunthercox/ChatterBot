from tests.base_case import ChatBotTestCase
from chatterbot.logic import LogicAdapter
from chatterbot.conversation import Statement


class ChatterBotResponseTestCase(ChatBotTestCase):

    def test_conversation_values_persisted_to_response(self):
        response = self.chatbot.get_response('Hello', persist_values_to_response={
            'conversation': 'test 1'
        })
        self.assertEqual(response.conversation, 'test 1')

    def test_tag_values_persisted_to_response(self):
        response = self.chatbot.get_response('Hello', persist_values_to_response={
            'tags': [
                'tag 1',
                'tag 2'
            ]
        })
        self.assertEqual(len(response.tags), 2)
        self.assertIn('tag 1', response.get_tags())
        self.assertIn('tag 2', response.get_tags())

    def test_in_response_to_provided(self):
        """
        Test that the process of looking up the previous response
        in the conversation is ignored if a previous response is provided.
        """
        self.chatbot.get_response(
            text='Hello',
            in_response_to='Unique previous response.'
        )
        statement = self.chatbot.storage.filter(
            text='Hello',
            in_response_to='Unique previous response.'
        )
        self.assertIsNotNone(statement)

    def test_no_statements_known(self):
        """
        If there is no statements in the database, then the
        user's input is the only thing that can be returned.
        """
        statement_text = 'How are you?'
        response = self.chatbot.get_response(statement_text)
        results = list(self.chatbot.storage.filter(text=statement_text))

        self.assertEqual(response.text, statement_text)
        self.assertEqual(response.confidence, 0)

        # Make sure that the input and output were saved
        self.assertIsLength(results, 2)
        self.assertEqual(results[0].text, statement_text)
        self.assertEqual(results[1].text, statement_text)

    def test_one_statement_known_no_response(self):
        """
        Test the case where a single statement is known, but
        it is not in response to any other statement.
        """
        self.chatbot.storage.create(text='Hello', in_response_to=None)

        response = self.chatbot.get_response('Hi')

        self.assertEqual(response.confidence, 0)
        self.assertEqual(response.text, 'Hello')

    def test_one_statement_one_response_known(self):
        """
        Test the case that one response is known and there is a response
        entry for it in the database.
        """
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')

        response = self.chatbot.get_response('Hi')

        self.assertEqual(response.confidence, 0)
        self.assertEqual(response.text, 'Hello')

    def test_two_statements_one_response_known(self):
        """
        Test the case that one response is known and there is a response
        entry for it in the database.
        """
        self.chatbot.storage.create(text='Hi', in_response_to=None)
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')

        response = self.chatbot.get_response('Hi')

        self.assertEqual(response.confidence, 1)
        self.assertEqual(response.text, 'Hello')

    def test_three_statements_two_responses_known(self):
        self.chatbot.storage.create(text='Hi', in_response_to=None)
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')
        self.chatbot.storage.create(text='How are you?', in_response_to='Hello')

        first_response = self.chatbot.get_response('Hi')
        second_response = self.chatbot.get_response('How are you?')

        self.assertEqual(first_response.confidence, 1)
        self.assertEqual(first_response.text, 'Hello')
        self.assertEqual(second_response.confidence, 0)

    def test_four_statements_three_responses_known(self):
        self.chatbot.storage.create(text='Hi', in_response_to=None)
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')
        self.chatbot.storage.create(text='How are you?', in_response_to='Hello')
        self.chatbot.storage.create(text='I am well.', in_response_to='How are you?')

        first_response = self.chatbot.get_response('Hi')
        second_response = self.chatbot.get_response('How are you?')

        self.assertEqual(first_response.confidence, 1)
        self.assertEqual(first_response.text, 'Hello')
        self.assertEqual(second_response.confidence, 1)
        self.assertEqual(second_response.text, 'I am well.')

    def test_second_response_unknown(self):
        self.chatbot.storage.create(text='Hi', in_response_to=None)
        self.chatbot.storage.create(text='Hello', in_response_to='Hi')

        first_response = self.chatbot.get_response(
            text='Hi',
            conversation='test'
        )
        second_response = self.chatbot.get_response(
            text='How are you?',
            conversation='test'
        )

        results = list(self.chatbot.storage.filter(text='How are you?'))

        self.assertEqual(first_response.confidence, 1)
        self.assertEqual(first_response.text, 'Hello')
        self.assertEqual(first_response.in_response_to, 'Hi')

        self.assertEqual(second_response.confidence, 0)
        self.assertEqual(second_response.in_response_to, 'How are you?')

        # Make sure that the second response was saved to the database
        self.assertIsLength(results, 1)
        self.assertEqual(results[0].in_response_to, 'Hi')

    def test_statement_added_to_conversation(self):
        """
        An input statement should be added to the recent response list.
        """
        statement = Statement(text='Wow!', conversation='test')
        response = self.chatbot.get_response(statement)

        self.assertEqual(statement.text, response.text)
        self.assertEqual(response.conversation, 'test')

    def test_get_response_additional_response_selection_parameters(self):
        self.chatbot.storage.create_many([
            Statement('A', conversation='test_1'),
            Statement('B', conversation='test_1', in_response_to='A'),
            Statement('A', conversation='test_2'),
            Statement('C', conversation='test_2', in_response_to='A'),
        ])

        statement = Statement(text='A', conversation='test_3')
        response = self.chatbot.get_response(statement, additional_response_selection_parameters={
            'conversation': 'test_2'
        })

        self.assertEqual(response.text, 'C')
        self.assertEqual(response.conversation, 'test_3')

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
        self.chatbot.get_response(Statement(
            text='Hello',
            in_response_to='Hi',
            tags=['test']
        ))

        results = list(self.chatbot.storage.filter(text='Hello'))

        self.assertIsLength(results, 2)
        self.assertIn('test', results[0].get_tags())
        self.assertEqual(results[1].get_tags(), [])

    def test_get_response_with_text_and_kwargs(self):
        self.chatbot.get_response('Hello', conversation='greetings')

        results = list(self.chatbot.storage.filter(text='Hello'))

        self.assertIsLength(results, 2)
        self.assertEqual(results[0].conversation, 'greetings')
        self.assertEqual(results[1].conversation, 'greetings')

    def test_get_response_missing_text(self):
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response()

    def test_get_response_missing_text_with_conversation(self):
        with self.assertRaises(self.chatbot.ChatBotException):
            self.chatbot.get_response(conversation='test')

    def test_generate_response(self):
        statement = Statement(text='Many insects adopt a tripedal gait for rapid yet stable walking.')
        response = self.chatbot.generate_response(statement)

        self.assertEqual(response.text, statement.text)
        self.assertEqual(response.confidence, 0)

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
            search_text=self.chatbot.storage.tagger.get_text_index_string(
                'Example A for search.'
            )
        ))

        self.assertEqual(len(results), 1)
        self.assertEqual('Example A for search.', results[0].text)


class TestAdapterA(LogicAdapter):

    def process(self, statement, additional_response_selection_parameters=None):
        response = Statement(text='Good morning.')
        response.confidence = 0.2
        return response


class TestAdapterB(LogicAdapter):

    def process(self, statement, additional_response_selection_parameters=None):
        response = Statement(text='Good morning.')
        response.confidence = 0.5
        return response


class TestAdapterC(LogicAdapter):

    def process(self, statement, additional_response_selection_parameters=None):
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
        self.assertEqual(statement.text, 'Good morning.')

    def test_chatbot_set_for_all_logic_adapters(self):
        for sub_adapter in self.chatbot.logic_adapters:
            self.assertEqual(sub_adapter.chatbot, self.chatbot)
        self.assertGreater(
            len(self.chatbot.logic_adapters), 0,
            msg='At least one logic adapter is expected for this test.'
        )

    def test_response_persona_is_bot(self):
        """
        The response returned from the chatbot should be set to the name of the chatbot.
        """
        response = self.chatbot.get_response('Hey everyone!')

        self.assertEqual(response.persona, 'bot:Test Bot')
