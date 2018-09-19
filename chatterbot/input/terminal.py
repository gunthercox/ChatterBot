from chatterbot.input import InputAdapter
from chatterbot.conversation import Statement


class TerminalAdapter(InputAdapter):
    """
    A simple adapter that allows ChatterBot to
    communicate through the terminal.
    """

    def process_input(self, *args):
        """
        Read the user's input from the terminal.
        """
        user_input = input()
        return Statement(user_input)
