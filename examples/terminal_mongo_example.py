from chatterbot import ChatBot


# Create a new ChatBot instance
bot = ChatBot("Terminal",
    storage_adapter="chatterbot.adapters.storage.MongoDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    input_adapter="chatterbot.adapters.input.TerminalAdapter",
    output_adapter="chatterbot.adapters.output.TerminalAdapter",
    database="chatterbot-database"
)

print("Type something to begin...")

while True:
    try:
        bot_input = bot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
