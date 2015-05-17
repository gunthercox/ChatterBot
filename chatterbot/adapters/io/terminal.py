from chatterbot.adapters.io import IOAdapter


class TerminalAdapter(object):

    def get_output(self, input_value):
        # 'raw_input' is just 'input' in python3
        if sys.version_info[0] < 3:
            user_input = str(raw_input())
        else:
            user_input = input()

        bot_input = chatbot.get_response(user_input)
        print(bot_input)

        return bot_input
