from chatterbot.adapters.io import IOAdapter


class TerminalAdapter(IOAdapter):

    def get_response(self, chatbot, input_text, user_name):

        response = chatbot.get_response_data(user_name, input_text)["bot"]

        print(response)
        return response
