from .base_case import ChatBotTestCase
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

        conversation.statements = [s1, s2]

        self.assertEqual(len(conversation), 2)

    def test_conversation_is_iterable(self):
        conversation = Conversation()

        count = 0

        s1 = Statement("Bilbo", "Good Morning!")
        s2 = Statement("Gandalf", "What do you mean?")

        conversation.statements = [s1, s2]

        for statement in conversation:
            count += 1

        self.assertEqual(count, 2)

    def test_add(self):
        conversation = Conversation()

        s1 = Statement("Bilbo", "Go away!")
        conversation.add(s1)

        self.assertEqual(len(conversation), 1)

    def test_next_line(self):
        conversation = Conversation()

        s1 = Statement("Bilbo", "Good Morning!")
        s2 = Statement("Gandalf", "What do you mean?")
        s3 = Statement("Bilbo", "I mean it's a good morning whether you want it or not.")

        conversation.statements = [s1, s2, s3]

        index = 0
        next_line, next_index = conversation.next_line(index)

        self.assertEqual(next_line.text, s2.text)
        self.assertEqual(next_index, index + 1)

    def test_find_closest_response_exact_match(self):
        conversation = Conversation()

        s1 = Statement("Bilbo", "Good Morning!")
        s2 = Statement("Gandalf", "What do you mean?")
        s3 = Statement("Bilbo", "I mean it's a good morning whether you want it or not.")
        s4 = Statement("Gandalf", "Good morning then.")

        conversation.statements = [s1, s2, s3, s4]

        response, ratio = conversation.find_closest_response(s1.text)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].text, s2.text)
        self.assertEqual(ratio, 100)

    def test_find_closest_response_loose_match(self):
        conversation = Conversation()

        s1 = Statement("Bilbo", "Good Morning!")
        s2 = Statement("Gandalf", "What do you mean?")
        s3 = Statement("Bilbo", "I mean it's a good morning whether you want it or not.")
        s4 = Statement("Gandalf", "Good morning then.")

        conversation.statements = [s1, s2, s3, s4]

        response, ratio = conversation.find_closest_response("What?")

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].text, s3.text)

    def test_find_closest_response_return_multiple_lines(self):
        conversation = Conversation()

        s1 = Statement("Gandalf", "What is your definition of relativity?")
        s2 = Statement("Albert Einstein", "When you are courting a nice girl an hour seems like a second.")
        s3 = Statement("Albert Einstein", "When you sit on a red-hot cinder a second seems like an hour.")
        s4 = Statement("Albert Einstein", "That's relativity.")

        conversation.statements = [s1, s2, s3, s4]

        response, ratio = conversation.find_closest_response(s1.text)

        self.assertEqual(len(response), 3)
        self.assertEqual(response[0].text, s2.text)
        self.assertEqual(response[1].text, s3.text)
        self.assertEqual(response[2].text, s4.text)
