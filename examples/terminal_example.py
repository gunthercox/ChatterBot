from chatterbot import ChatBot

'''
In this example we use a while loop combined with a try-except statement.
This allows us to have a conversation with the chat bot until we press
ctrl-c or ctrl-d on the keyboard.
'''

# Create a new instance of a ChatBot
bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.EvaluateMathematically",
        "chatterbot.adapters.logic.TimeLogicAdapter",
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    input_adapter="chatterbot.adapters.input.TerminalAdapter",
    output_adapter="chatterbot.adapters.output.TerminalAdapter",
    database="../database.db"
)

# Text to prompt the user with initially
user_input = "Type something to begin..."

print(user_input)

while True:
    try:
        # We pass None to this method because it expects a response.
        # The TerminalAdapter will handle reading from the user's terminal.
        bot_input = bot.get_response(None)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
