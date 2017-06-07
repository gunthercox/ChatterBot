# -*- coding: utf-8 -*-
from chatterbot import ChatBot


# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new ChatBot instance

bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.ArangoStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    filters=[
        'chatterbot.filters.RepetitiveResponseFilter'
    ],
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    username='chatterbot',  # Enter user name here (required)
    password='chatterbot',  # Enter password here (required)
    database='chatterbot-database',  # Enter database name here (default: chatterbot-database)
    collection='statements',  # Enter collection name here (default: statements)
    host='localhost',  # Enter host name (default: localhost)
    port='8529',  # Enter port name (default: 8529)
    protocol='http',  # Enter protocol name (default: http)
    logging=True  # Enter logging condition (default: True)
)

print('Type something to begin...')

while True:
    try:
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
