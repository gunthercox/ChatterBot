from chatterbot import ChatBot


bot = ChatBot("Training Example",
    storage_adapter="chatterbot.adapters.storage.JsonDatabaseAdapter",
    logic_adapter="chatterbot.adapters.logic.ClosestMatchAdapter",
    io_adapter="chatterbot.adapters.io.TerminalAdapter",
    database="./new_database.db")

'''
Give the chat bot a sample conversation to help
it learn how to respond to different statements.
'''
training_data = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm great.",
    "That is good to hear",
    "Thank you.",
    "Your welcome.",
    "Sure, any time.",
    "Yeah",
    "Can I help you with anything?"
]

bot.train(training_data)

user_input = ""

while True:
    try:
        user_input = bot.get_input()

        bot_input = bot.get_response(user_input)

    except (KeyboardInterrupt, EOFError, SystemExit):
        break

