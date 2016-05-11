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
    logic_adapters=[
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    input_adapter="chatterbot.adapters.input.TerminalAdapter",
    output_adapter="chatterbot.adapters.output.TerminalAdapter",
    database="../database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)

print("Type something to begin...")

while True:
    try:
        bot_input = chatbot.get_response(None)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
