from chatterbot import ChatBot
from settings import TWITTER


'''
To use this example, create a new file called settings.py.
In settings.py define the following:

TWITTER = {
    "CONSUMER_KEY": "my-twitter-consumer-key",
    "CONSUMER_SECRET": "my-twitter-consumer-secret",
    "ACCESS_TOKEN": "my-access-token",
    "ACCESS_TOKEN_SECRET": "my-access-token-secret"
}
'''


chatbot = ChatBot("ChatterBot",
    storage_adapter="chatterbot.adapters.storage.TwitterAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="../database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)

user_input = "Type something to begin..."

print(user_input)

while True:
    try:
        user_input = chatbot.get_input()
        bot_input = chatbot.get_response(user_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

