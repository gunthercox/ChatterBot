from chatterbot import ChatBot


# Create a new instance of a ChatBot
bot = ChatBot("No Output",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.ClosestMeaningAdapter"
    ],
    input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.adapters.output.OutputFormatAdapter",
    database="../database.db")

'''
Manipulating the above statement allows you to edit the
configuration to make use of different aspects of the
library. Please see the wiki for in-depth information on
how to configure ChatterBot.
'''

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
        the bot's output should be returned. In the case of the NoOutputAdapter,
        the output is not printed to the terminal.
        '''
        bot_input = bot.get_response(None)

        print(bot_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
