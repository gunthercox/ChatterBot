from chatterbot import ChatBot
import logging
from chatterbot.trainers import ChatterBotCorpusTrainer

# Uncomment the following line to enable verbose logging
# logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
bot = ChatBot("Terminal",
    storage_adapter="chatterbot.storage.JsonFileStorageAdapter",
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter"
)
bot.set_trainer(ChatterBotCorpusTrainer)

bot.train(
    "chatterbot.corpus.english"
)

DEFAULT_SESSION_ID = bot.default_session.id

def get_feedback():
    from chatterbot.utils import input_function

    text = input_function()

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
               input_statement = bot.input.process_input_statement()
               statement, response = bot.generate_response(input_statement, DEFAULT_SESSION_ID)
               bot.output.process_response(response)
               print('\n Is "{}" a coherent response to "{}"? \n'.format(response, input_statement))                      
               if get_feedback():
                    print("please input the correct one")
                    response1 = bot.input.process_input_statement()
                    bot.learn_response(response1, input_statement)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
