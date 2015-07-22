# -*- coding: utf-8 -*-
from .base_case import ChatBotTestCase, UntrainedChatBotTestCase
from chatterbot import ChatBot


class ChatBotOutputTests(ChatBotTestCase):

    def test_training_adds_statements(self):
        """
        Test that the training method adds statements to the database.
        """
        import os

        bot = ChatBot("Test Bot2", database="test-database-2")

        conversation = [
            "Hello",
            "Hi there!",
            "How are you doing?",
            "I'm great.",
            "That is good to hear",
            "Thank you.",
            "You are welcome.",
            "Sure, any time.",
            "Yeah",
            "Can I help you with anything?"
        ]

        bot.train(conversation)

        response = bot.get_response("Thank you.")

        os.remove("test-database-2")

        self.assertEqual(response, "You are welcome.")

    def test_training_increments_occurrence_count(self):

        conversation = [
            "Do you like my hat?",
            "I do not like your hat."
        ]

        self.chatbot.train(conversation)
        self.chatbot.train(conversation)

        count = self.chatbot.storage.storage_adapter.find("Do you like my hat?")["occurrence"]
        self.assertEqual(count, 2)

    def test_answer_to_known_input(self):
        """
        Test that a matching response is returned when an
        exact match exists in the database.
        """
        input_text = "What... is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        self.assertIn("Blue", response)

    def test_answer_close_to_known_input(self):

        input_text = "What is your favourite colour?"
        response = self.chatbot.get_response(input_text)

        self.assertIn("Blue", response)

    def test_match_has_no_response(self):
        """
        Make sure that the if the last line in a file
        matches the input text then a index error does
        not occure.
        """
        input_text = "Siri is my cat"
        response = self.chatbot.get_response(input_text)

        self.assertGreater(len(response), 0)

    def test_input_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        user name, timestamp and input text
        """
        user_name = "Ron Obvious"
        user_input = "Hello!"

        data = self.chatbot.get_response_data({"name": user_name, "text": user_input})

        self.assertIn(user_input, data[user_name].keys())

    def test_output_text_returned_in_response_data(self):
        """
        This checks to see if a value is returned for the
        bot name, timestamp and input text
        """
        user_name = "Sherlock"
        user_input = "Elementary my dear watson."

        data = self.chatbot.get_response_data({"name": user_name, "text": user_input})

        self.assertGreater(len(data["bot"]), 0)

    def test_training_with_unicode_characters(self):
        """
        Ensure that the training method adds unicode statements
        to the database.
        """
        import os

        bot = ChatBot("Test Bot2", database="unicode-database.db")

        conversation = [
            u"¶ ∑ ∞ ∫ π ∈ ℝ² ∖ ⩆ ⩇ ⩈ ⩉ ⩊ ⩋ ⪽ ⪾ ⪿ ⫀ ⫁ ⫂ ⋒ ⋓",
            u"⊂ ⊃ ⊆ ⊇ ⊈ ⊉ ⊊ ⊋ ⊄ ⊅ ⫅ ⫆ ⫋ ⫌ ⫃ ⫄ ⫇ ⫈ ⫉ ⫊ ⟃ ⟄",
            u"∠ ∡ ⦛ ⦞ ⦟ ⦢ ⦣ ⦤ ⦥ ⦦ ⦧ ⦨ ⦩ ⦪ ⦫ ⦬ ⦭ ⦮ ⦯ ⦓ ⦔ ⦕ ⦖ ⟀",
            u"∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳ ⨋ ⨌ ⨍ ⨎ ⨏ ⨐ ⨑ ⨒ ⨓ ⨔ ⨕ ⨖ ⨗ ⨘ ⨙ ⨚ ⨛ ⨜",
            u"≁ ≂ ≃ ≄ ⋍ ≅ ≆ ≇ ≈ ≉ ≊ ≋ ≌ ⩯ ⩰ ⫏ ⫐ ⫑ ⫒ ⫓ ⫔ ⫕ ⫖",
            u"¬ ⫬ ⫭ ⊨ ⊭ ∀ ∁ ∃ ∄ ∴ ∵ ⊦ ⊬ ⊧ ⊩ ⊮ ⊫ ⊯ ⊪ ⊰ ⊱ ⫗ ⫘",
            u"∧ ∨ ⊻ ⊼ ⊽ ⋎ ⋏ ⟑ ⟇ ⩑ ⩒ ⩓ ⩔ ⩕ ⩖ ⩗ ⩘ ⩙ ⩚ ⩛ ⩜ ⩝ ⩞ ⩟ ⩠ ⩢",
        ]

        bot.train(conversation)

        response = bot.get_response(conversation[1])

        os.remove("unicode-database.db")

        self.assertEqual(response, conversation[2])

    def test_empty_input(self):
        """
        If empty input is provided, anything may be returned.
        """
        output = self.chatbot.get_response("")

        self.assertTrue(len(output) > -1)


class ResponseTestCase(UntrainedChatBotTestCase):

    def test_empty_database(self):
        """
        If there is no statements in the database, then the
        user's input is the only thing that can be returned.
        """
        response = self.chatbot.get_response("How are you?")

        self.assertEqual("How are you?", response)


class DatabaseTests(UntrainedChatBotTestCase):

    def test_database_is_updated(self):
        """
        Test that the database is updated when logging is set to true.
        """
        self.chatbot.log = True

        input_text = "What is the airspeed velocity of an unladen swallow?"
        exists_before = self.chatbot.storage.storage_adapter.find(input_text)

        response = self.chatbot.get_response(input_text)
        exists_after = self.chatbot.storage.storage_adapter.find(input_text)

        self.assertFalse(exists_before)
        self.assertTrue(exists_after)

    def test_database_is_not_updated_when_logging_is_disabled(self):
        """
        Test that the database is not updated when logging is set to false.
        """
        self.chatbot.log = False

        input_text = "Who are you? The proud lord said."
        exists_before = self.chatbot.storage.storage_adapter.find(input_text)

        response = self.chatbot.get_response(input_text)
        exists_after = self.chatbot.storage.storage_adapter.find(input_text)

        self.assertFalse(exists_before)
        self.assertFalse(exists_after)
