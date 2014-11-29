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

    def test_update_timestamp(self):
        import time

        statement = Statement("bot", "You stand with us... or you stand against me.")

        date = statement.date

        time.sleep(0.0001)
        statement.update_timestamp()

        update = statement.date

        self.assertNotEqual(date, update)

    def test_update_name(self):

        statement = Statement("bot", "Freedom is the right of all sentient beings.")
        statement.set_name("Optimus")

        self.assertEqual(statement.name, "Optimus")


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
