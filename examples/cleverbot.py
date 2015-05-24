from chatterbot import ChatBot
from chatterbot.cleverbot.cleverbot import Cleverbot
from chatterbot.apis import clean
from random import randint
import time

bot = ChatBot("Chatterbot",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.EngramAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="../clever-database.db", logging=True)

    cleverbot = Cleverbot()

    bot_input = "Hi. How are you?"

    print(bot.name, bot_input)

    while True:
        cb_input = cleverbot.ask(bot_input)
        print("cleverbot:", cb_input)
        cb_input = clean(cb_input)

        bot_input = bot.get_response(cb_input, "cleverbot")
        print(bot.name, bot_input)
        bot_input = clean(bot_input)

        # Delay a random number of seconds.
        time.sleep(1.05 + randint(0, 9))
