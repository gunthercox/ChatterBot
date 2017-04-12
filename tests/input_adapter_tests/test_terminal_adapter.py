from unittest import TestCase
from chatterbot.conversation import Statement
from chatterbot.input import TerminalAdapter


class TerminalAdapterTests(TestCase):
    """
    The terminal adapter is designed to allow
    interaction with the chat bot to occur through
    a command line interface.
    """

    def setUp(self):
        self.adapter = TerminalAdapter()
