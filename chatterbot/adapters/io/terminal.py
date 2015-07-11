from chatterbot.adapters.io import IOAdapter


class TerminalAdapter(IOAdapter):

    def get_response(self, chatbot, input_data):

        response = chatbot.get_response_data(input_data)

        bot_response = response["bot"]

        bot_response_text = list(bot_response.keys())[0]

        print(bot_response_text)
        return bot_response_text
