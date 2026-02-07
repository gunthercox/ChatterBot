from unittest import TestCase
from tests.base_case import ChatBotTestCase
from chatterbot import ChatBot
from chatterbot.conversation import Statement


class StatementTests(TestCase):

    def setUp(self):
        self.statement = Statement(text='A test statement.')

    def test_serializer(self):
        data = self.statement.serialize()
        self.assertEqual(self.statement.text, data['text'])


class DefaultConversationTestCase(ChatBotTestCase):
    """
    Test that the ChatBot assigns a default conversation ID when none is
    provided, so that LLM adapters can retrieve conversation history.
    """

    def test_default_conversation_is_set(self):
        """
        The ChatBot should have a default_conversation attribute
        that is a 32-character hex string (UUID without hyphens).
        """
        self.assertIsNotNone(self.chatbot.default_conversation)
        self.assertEqual(len(self.chatbot.default_conversation), 32)
        # Verify it's a valid hex string
        int(self.chatbot.default_conversation, 16)

    def test_default_conversation_is_unique_per_instance(self):
        """
        Each ChatBot instance should generate a unique conversation ID.
        """
        kwargs = self.get_kwargs()
        kwargs['tagger'] = self._shared_tagger
        other_bot = ChatBot('Other Bot', **kwargs)

        self.assertNotEqual(
            self.chatbot.default_conversation,
            other_bot.default_conversation
        )

        other_bot.storage.drop()
        other_bot.storage.close()

    def test_response_gets_default_conversation(self):
        """
        When no conversation kwarg is passed, the response should
        have the chatbot's default_conversation ID assigned.
        """
        response = self.chatbot.get_response('Hello')
        self.assertEqual(response.conversation, self.chatbot.default_conversation)

    def test_explicit_conversation_overrides_default(self):
        """
        When an explicit conversation ID is provided, it should be
        used instead of the default_conversation.
        """
        response = self.chatbot.get_response('Hello', conversation='my-convo')
        self.assertEqual(response.conversation, 'my-convo')

    def test_statement_object_conversation_overrides_default(self):
        """
        When a Statement object with a conversation ID is provided,
        it should be used instead of the default_conversation.
        """
        statement = Statement(text='Hello', conversation='custom-id')
        response = self.chatbot.get_response(statement)
        self.assertEqual(response.conversation, 'custom-id')

    def test_empty_conversation_gets_default(self):
        """
        When a Statement object with an empty conversation string is
        provided, the default should be applied as a fallback.
        """
        statement = Statement(text='Hello')
        # Statement defaults to '' for conversation
        self.assertEqual(statement.conversation, '')

        response = self.chatbot.get_response(statement)
        self.assertEqual(response.conversation, self.chatbot.default_conversation)

    def test_statements_saved_with_default_conversation(self):
        """
        Both the input and response statements should be saved
        to storage with the default conversation ID.
        """
        self.chatbot.get_response('Hello')
        results = list(self.chatbot.storage.filter(
            conversation=self.chatbot.default_conversation
        ))
        # Should have at least the input and the response
        self.assertGreaterEqual(len(results), 2)

    def test_conversation_history_accumulates(self):
        """
        Multiple calls with the same default conversation should
        accumulate in storage, allowing history retrieval.
        """
        self.chatbot.get_response('First message')
        self.chatbot.get_response('Second message')

        results = list(self.chatbot.storage.filter(
            conversation=self.chatbot.default_conversation,
            order_by=['id']
        ))

        # Each get_response saves the input + learned response = 2 per call
        # so 2 calls should produce at least 4 statements
        self.assertGreaterEqual(len(results), 4)

        texts = [r.text for r in results]
        self.assertIn('First message', texts)
        self.assertIn('Second message', texts)
