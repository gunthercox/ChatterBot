from chatterbot import ChatBot

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot(
    'SQLMemoryTerminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri=None,
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch'
    ]
)

# Get a few responses from the bot

bot.get_response('What time is it?')

bot.get_response('What is 7 plus 7?')
