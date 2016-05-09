from chatterbot import ChatBot


# Create a new instance of a ChatBot
bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="chatterbot-database")

print("Type something to begin...")

'''
In this example we use a while loop combined with a try-except statement.
This allows us to have a conversation with the chat bot until we press
ctrl-c or ctrl-d on the keyboard.
'''

while True:
    try:
        '''
        The get_response method also uses the io adapter to determine how
        the bot's output should be returned. In the case of the TerminalAdapter,
        the output is printed to the user's terminal.
        '''
        bot_input = bot.get_response(None)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

