from .test_case import ChatBotTestCase
from chatterbot.conversation import Statement, Conversation


class StatementTests(ChatBotTestCase):

    def test_string_is_text_value(self):

        text = "I am a robot."

        statement = Statement("bot", text)

        self.assertEqual(str(statement), text)

    def test_statement_automatic_date(self):
        import datetime

        statement = Statement("bot", "Hows it going?")

        self.assertEqual(type(statement.date), datetime.datetime)

    def test_statement_set_response(self):

        first = Statement("bob", "How are you?")
        second = Statement("sam", "I am good.")
        second.in_response_to(first)

        self.assertEqual(second.response_to, first)


class ConversationTests(ChatBotTestCase):

    def test_conversation_has_len_of_statement(self):
        conversation = Conversation()

        s1 = Statement("Bilbo", "Good Morning!")
        s2 = Statement("Gandalf", "What do you mean?")

        conversation.add(s1)
        conversation.add(s2)

        self.assertEqual(len(conversation), 2)

    def test_conversation_is_iterable(self):
        conversation = Conversation()

        count = 0

        s1 = Statement("Bilbo", "Good Morning!")
        s2 = Statement("Gandalf", "What do you mean?")

        conversation.add(s1)
        conversation.add(s2)

        for statement in conversation:
            count += 1

        self.assertEqual(count, 2)
