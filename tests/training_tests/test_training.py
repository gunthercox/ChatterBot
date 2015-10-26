# -*- coding: utf-8 -*-
from tests.base_case import UntrainedChatBotTestCase 


class TrainingTestCase(UntrainedChatBotTestCase):

    def test_training_adds_statements(self):
        """
        Test that the training method adds statements to the database.
        """
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

        self.chatbot.train(conversation)

        response = self.chatbot.get_response("Thank you.")

        self.assertEqual(response, "You are welcome.")

    '''
    # TODO
    def test_training_increments_occurrence_count(self):

        conversation = [
            "Do you like my hat?",
            "I do not like your hat."
        ]

        self.chatbot.train(conversation)
        self.chatbot.train(conversation)

        statement = self.chatbot.storage.find("Do you like my hat?")
        self.assertEqual(statement.get_occurrence_count(), 2)
    '''

    def test_database_has_correct_format(self):
        """
        Test that the database maintains a valid format
        when data is added and updated. This means that
        after the training process, the database should
        contain nine objects and eight of these objects
        should list the previous member of the list as
        a response.
        """
        conversation = [
            "Hello sir!",
            "Hi, can I help you?",
            "Yes, I am looking for italian parsely.",
            "Italian parsely is right over here in out produce department",
            "Great, thank you for your help.",
            "No problem, did you need help finding anything else?",
            "Nope, that was it.",
            "Alright, have a great day.",
            "Thanks, you too."
        ]

        self.chatbot.train(conversation)

        # There should be a total of 9 statements in the database after training
        self.assertEqual(self.chatbot.storage.count(), 9)

        # The first statement should be in responce to another statement yet
        self.assertEqual(
            len(self.chatbot.storage.find(conversation[0]).in_response_to),
            0
        )

        # The second statement should have one response
        self.assertEqual(
            len(self.chatbot.storage.find(conversation[1]).in_response_to),
            1
        )

        # The second statement should be in response to the first statement
        self.assertIn(
            conversation[0],
            self.chatbot.storage.find(conversation[1]).in_response_to,
        )

    def test_training_with_unicode_characters(self):
        """
        Ensure that the training method adds unicode statements
        to the database.
        """
        conversation = [
            u"¶ ∑ ∞ ∫ π ∈ ℝ² ∖ ⩆ ⩇ ⩈ ⩉ ⩊ ⩋ ⪽ ⪾ ⪿ ⫀ ⫁ ⫂ ⋒ ⋓",
            u"⊂ ⊃ ⊆ ⊇ ⊈ ⊉ ⊊ ⊋ ⊄ ⊅ ⫅ ⫆ ⫋ ⫌ ⫃ ⫄ ⫇ ⫈ ⫉ ⫊ ⟃ ⟄",
            u"∠ ∡ ⦛ ⦞ ⦟ ⦢ ⦣ ⦤ ⦥ ⦦ ⦧ ⦨ ⦩ ⦪ ⦫ ⦬ ⦭ ⦮ ⦯ ⦓ ⦔ ⦕ ⦖ ⟀",
            u"∫ ∬ ∭ ∮ ∯ ∰ ∱ ∲ ∳ ⨋ ⨌ ⨍ ⨎ ⨏ ⨐ ⨑ ⨒ ⨓ ⨔ ⨕ ⨖ ⨗ ⨘ ⨙ ⨚ ⨛ ⨜",
            u"≁ ≂ ≃ ≄ ⋍ ≅ ≆ ≇ ≈ ≉ ≊ ≋ ≌ ⩯ ⩰ ⫏ ⫐ ⫑ ⫒ ⫓ ⫔ ⫕ ⫖",
            u"¬ ⫬ ⫭ ⊨ ⊭ ∀ ∁ ∃ ∄ ∴ ∵ ⊦ ⊬ ⊧ ⊩ ⊮ ⊫ ⊯ ⊪ ⊰ ⊱ ⫗ ⫘",
            u"∧ ∨ ⊻ ⊼ ⊽ ⋎ ⋏ ⟑ ⟇ ⩑ ⩒ ⩓ ⩔ ⩕ ⩖ ⩗ ⩘ ⩙ ⩚ ⩛ ⩜ ⩝ ⩞ ⩟ ⩠ ⩢",
        ]

        self.chatbot.train(conversation)

        response = self.chatbot.get_response(conversation[1])

        self.assertEqual(response, conversation[2])

    def test_similar_sentence_gets_same_response_multiple_times(self):
        """
        Tests if the bot returns the same response for the same question (which is similar to the one 
        present in the training set) when asked repeatedly.
        Also, it checks if the question is added to the in_response_to array in db for the response.
        """
        training = [
            'how do you login to gmail?',
            'Goto gmail.com, enter your login information and hit enter!'
        ]

        similar_question = 'how do I login to gmail?'

        self.chatbot.train(training)
        response_to_trained_set = self.chatbot.get_response('how do you login to gmail?')
        response_to_similar_question_1 = self.chatbot.get_response(similar_question)
        response_to_similar_question_2 = self.chatbot.get_response(similar_question)

        self.assertEqual(response_to_trained_set, response_to_similar_question_1)
        self.assertEqual(response_to_similar_question_1, response_to_similar_question_2)
        self.assertIn(similar_question, self.chatbot.storage.find(response_to_trained_set).in_response_to)
