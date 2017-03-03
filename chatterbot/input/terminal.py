from __future__ import unicode_literals
from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement
from chatterbot.utils import input_function


class TerminalAdapter(InputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_input(self, *args, **kwargs):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return Statement(user_input)
