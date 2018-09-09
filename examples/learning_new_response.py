from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


# Uncomment the following line to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

CONVERSATION = 'example_learning_conversation'

# Create a new instance of a ChatBot
bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter"
)
bot.set_trainer(ChatterBotCorpusTrainer)

bot.train("chatterbot.corpus.english")


def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return False
    elif 'no' in text.lower():
        return True
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        input_statement = bot.input.process_input()
        statement, response = bot.generate_response(
            input_statement,
            CONVERSATION
        )

        bot.output.process_response(response)
        print('\n Is "{}" a coherent response to "{}"? \n'.format(response, input_statement))
        if get_feedback():
            print("please input the correct one")
            response1 = bot.input.process_input()
            bot.learn_response(CONVERSATION, response1, input_statement)
            print("Responses added to bot!")

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
