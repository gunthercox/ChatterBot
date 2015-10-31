from chatterbot.adapters.io import IOAdapter
from chatterbot.utils.read_input import input_function


class TerminalAdapter(IOAdapter):

    def process_input(self):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return user_input

    def process_response(self, statement):
#        print(statement.text)
        return statement.text

