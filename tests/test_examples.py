from unittest import TestCase


class ExamplesSmokeTestCase(TestCase):
    """
    These are just basic tests that run each example
    to make sure no errors are triggered.
    """

    def test_basic_example(self):
        from examples import basic_example # NOQA

    def test_convert_units(self):
        from examples import convert_units # NOQA

    def test_default_response_example(self):
        from examples import default_response_example # NOQA

    def test_export_example(self):
        self.skipTest(
            'This is being skipped to avoid creating files during tests.'
        )

    def test_learning_feedback_example(self):
        self.skipTest(
            'This is being skipped because it contains '
            'a while loop in the code body and will not '
            'terminate on its own.'
        )

    def test_math_and_time(self):
        from examples import math_and_time # NOQA

    def test_memory_sql_example(self):
        from examples import memory_sql_example # NOQA

    def test_specific_response_example(self):
        from examples import specific_response_example # NOQA

    def test_tagged_dataset_example(self):
        from examples import tagged_dataset_example # NOQA

    def test_terminal_example(self):
        self.skipTest(
            'This is being skipped because it contains '
            'a while loop in the code body and will not '
            'terminate on its own.'
        )

    def test_terminal_mongo_example(self):
        self.skipTest(
            'This is being skipped so that we do not have '
            'to check if Mongo DB is running before running '
            'this test.'
        )

    def test_tkinter_gui(self):
        self.skipTest(
            'This is being skipped so that we do not open up '
            'a GUI during testing.'
        )

    def test_training_example_chatterbot_corpus(self):
        from examples import training_example_chatterbot_corpus # NOQA

    def test_training_example_list_data(self):
        from examples import training_example_list_data # NOQA

    def test_training_example_ubuntu_corpus(self):
        self.skipTest(
            'This test is being skipped because it takes '
            'hours to download and train from this corpus.'
        )
