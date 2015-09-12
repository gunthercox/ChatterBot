from chatterbot import ChatBot
from settings import TWITTER


chatbot = ChatBot("ChatterBot",
    storage_adapter="chatterbot.adapters.storage.TwitterAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="../database.db",
    consumer_key=TWITTER["CONSUMER_KEY"],
    consumer_secret=TWITTER["CONSUMER_SECRET"]
)

'''
Respond to mentions on twitter.
The bot will follow the user who mentioned it and
favorite the post in which the mention was made.
'''

print chatbot.storage.get_random()



user_input = "Type something to begin..."

print(user_input)

while True:
    try:
        user_input = chatbot.get_input()

        bot_input = chatbot.get_response(user_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

