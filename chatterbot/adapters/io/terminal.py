from chatterbot.adapters.io import IOAdapter


class TerminalAdapter(IOAdapter):

    def process_response(self, response_data):

        bot_response = response_data["bot"]

        bot_response_text = list(bot_response.keys())[0]

        print(bot_response_text)
        return bot_response_text
