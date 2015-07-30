from chatterbot.adapters.io import IOAdapter
from chatterbot.utils.read_input import input_function


class TerminalAdapter(IOAdapter):

    def process_input(self):
        """
        Read the user's input from the terminal.
        """
        user_input = input_function()
        return user_input

    def process_response(self, response_data):

        bot_response = response_data["bot"]

        bot_response_text = list(bot_response.keys())[0]

        print(bot_response_text)
        return bot_response_text
