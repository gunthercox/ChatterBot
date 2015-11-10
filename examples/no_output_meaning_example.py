from chatterbot import ChatBot


# Create a new instance of a ChatBot
bot = ChatBot("No Output",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMeaningAdapter",
    io_adapter="chatterbot.adapters.io.NoOutputAdapter",
    database="../database.db")

'''
Manipulating the above statement allows you to edit the
configuration to make use of different aspects of the
library. Please see the wiki for in-depth information on
how to configure ChatterBot.
'''

user_input = "Type something to begin..."

# To make this Python 2.x compatible, replace the print() with print "enter print text here"
print(user_input)

'''
In this example we use a while loop combined with a try-except statement.
This allows us to have a conversation with the chat bot until we press
ctrl-c or ctrl-d on the keyboard.
'''

while True:
    try:
        '''
        ChatterBot's get_input method uses io adapter to get new input for
        the bot to respond to. In this example, the NoOutputAdapter gets the
        input from the user's terminal. Other io adapters might retrieve input
        differently, such as from various web APIs.
        '''
        user_input = bot.get_input()

        '''
        The get_response method also uses the io adapter to determine how
        the bot's output should be returned. In the case of the NoOutputAdapter,
        the output is not printed to the terminal.
        '''
        bot_input = bot.get_response(user_input)

        print(bot_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
