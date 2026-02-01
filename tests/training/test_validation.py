from tests.base_case import ChatBotTestCase
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from chatterbot import constants


class ListTrainingValidationTests(ChatBotTestCase):
    """
    Test validation parameter functionality for ListTrainer.
    """

    def test_validate_parameter_defaults_to_true(self):
        """
        Test that the validate parameter defaults to True.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False)
        self.assertTrue(trainer.validate)

    def test_validate_parameter_can_be_disabled(self):
        """
        Test that the validate parameter can be set to False.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False, validate=False)
        self.assertFalse(trainer.validate)

    def test_validation_rejects_text_exceeding_max_length(self):
        """
        Test that validation raises exception when text exceeds STATEMENT_TEXT_MAX_LENGTH.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False)

        long_text = "x" * (constants.STATEMENT_TEXT_MAX_LENGTH + 10)
        conversation = ["Hello", long_text, "Goodbye"]

        with self.assertRaises(trainer.TrainerInitializationException) as context:
            trainer.train(conversation)

        self.assertIn("exceeding maximum text length", str(context.exception))
        self.assertIn(str(constants.STATEMENT_TEXT_MAX_LENGTH), str(context.exception))
        self.assertIn("Statement at index 1", str(context.exception))

    def test_validation_includes_text_snippet_in_error(self):
        """
        Test that validation error includes a snippet of the problematic text.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False)

        long_text = "A" * (constants.STATEMENT_TEXT_MAX_LENGTH + 50)
        conversation = ["Hello", long_text]

        with self.assertRaises(trainer.TrainerInitializationException) as context:
            trainer.train(conversation)

        error_message = str(context.exception)
        # Should include snippet (first 100 chars + ellipsis)
        self.assertIn("A" * 100, error_message)
        self.assertIn("...", error_message)

    def test_validation_accepts_text_at_max_length(self):
        """
        Test that validation accepts text exactly at STATEMENT_TEXT_MAX_LENGTH.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False)

        max_length_text = "x" * constants.STATEMENT_TEXT_MAX_LENGTH
        conversation = ["Hello", max_length_text, "Goodbye"]

        # Should not raise exception
        trainer.train(conversation)

        response = self.chatbot.get_response("Hello")
        self.assertEqual(response.text, max_length_text)

    def test_validation_can_be_skipped(self):
        """
        Test that validation can be disabled for performance.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False, validate=False)

        long_text = "x" * (constants.STATEMENT_TEXT_MAX_LENGTH + 10)
        conversation = ["Hello", long_text]

        # Should not raise validation exception when validate=False
        # Note: May still fail at storage adapter level depending on backend
        try:
            trainer.train(conversation)
        except trainer.TrainerInitializationException:
            self.fail("TrainerInitializationException should not be raised when validate=False")

    def test_validation_checks_first_statement(self):
        """
        Test that validation checks the first statement in conversation.
        """
        trainer = ListTrainer(self.chatbot, show_training_progress=False)

        long_text = "x" * (constants.STATEMENT_TEXT_MAX_LENGTH + 5)
        conversation = [long_text, "Hello"]

        with self.assertRaises(trainer.TrainerInitializationException) as context:
            trainer.train(conversation)

        self.assertIn("Statement at index 0", str(context.exception))


class ChatterBotCorpusValidationTests(ChatBotTestCase):
    """
    Test validation parameter functionality for ChatterBotCorpusTrainer.
    """

    def test_corpus_trainer_inherits_validate_parameter(self):
        """
        Test that ChatterBotCorpusTrainer inherits the validate parameter.
        """
        trainer = ChatterBotCorpusTrainer(self.chatbot, show_training_progress=False)
        self.assertTrue(trainer.validate)

        trainer_no_validate = ChatterBotCorpusTrainer(
            self.chatbot, 
            show_training_progress=False, 
            validate=False
        )
        self.assertFalse(trainer_no_validate.validate)
