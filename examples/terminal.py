from chatterbot import ChatBot
import sys


bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.EngramAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="../database.db", logging=True)


conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm great.",
    "That is good to hear",
    "Thank you.",
    "Your welcome.",
    "Sure, any time.",
    "Yeah",
    "Can I help you with anything?"
]

bot.train(conversation)


user_input = "Type something to begin..."

print(user_input)

while True:
    try:
        # 'raw_input' is just 'input' in python3
        if sys.version_info[0] < 3:
            user_input = str(raw_input())
        else:
            user_input = input()

        bot_input = bot.get_response(user_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
