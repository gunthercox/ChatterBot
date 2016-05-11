from chatterbot import ChatBot


bot = ChatBot("Example",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapters=[
        "chatterbot.adapters.logic.ClosestMatchAdapter"
    ],
    input_adapter="chatterbot.adapters.input.VariableInputTypeAdapter",
    output_adapter="chatterbot.adapters.output.OutputFormatAdapter",
    database="../database.db"
)

print("Type something to begin...")

while True:
    try:
        bot_input = bot.get_response(None)
        print(bot_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break
