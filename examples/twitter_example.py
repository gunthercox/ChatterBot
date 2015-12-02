from chatterbot import ChatBot
from settings import TWITTER
import time

'''
The bot will respond to mentions and direct messages on twitter.
To use this example, create a new settings.py file.
Define the following in settings.py:

    TWITTER = {}
    TWITTER["CONSUMER_KEY"] = "your-twitter-public-key"
    TWITTER["CONSUMER_SECRET"] = "your-twitter-sceret-key"
'''


chatbot = ChatBot("ChatterBot",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TwitterAdapter",
    database="../database.db",
    twitter_consumer_key=TWITTER["CONSUMER_KEY"],
    twitter_consumer_secret=TWITTER["CONSUMER_SECRET"],
    twitter_access_token_key=TWITTER["ACCESS_TOKEN"],
    twitter_access_token_secret=TWITTER["ACCESS_TOKEN_SECRET"]
)

time.sleep(200)

'''
while True:
    try:
        user_input = chatbot.get_input()

        bot_input = chatbot.get_response(user_input)

        # Pause before checking for the next message
        time.sleep(25)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
'''
