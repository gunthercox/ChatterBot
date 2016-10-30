from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import logging


# Uncomment the following line to enable verbose logging
# logging.basicConfig(level=logging.INFO)

# Create a new ChatBot instance
chatterbot = ChatBot("Training Example",
    storage_adapter="chatterbot.adapters.storage.JsonFileStorageAdapter",
    #logic_adapters=[
        #"chatterbot.adapters.logic.MathematicalEvaluation",
        #"chatterbot.adapters.logic.TimeLogicAdapter",
        #"chatterbot.adapters.logic.ClosestMatchAdapter"
    #],
    input_adapter="chatterbot.adapters.input.TerminalAdapter",
    output_adapter="chatterbot.adapters.output.TerminalAdapter",
    database="../database.db"
)
chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train(
     "chatterbot.corpus.english.greetings",
     "chatterbot.corpus.english.conversations",
     #"chatterbot.corpus.english.math_words",
     #"chatterbot.corpus.english.trivia"
)

print("Type something to begin...")

# The following loop will execute each time the user enters input
while True:
    try:
        # We pass None to this method because the parameter
        # is not used by the TerminalAdapter
        chatterbot_input = chatterbot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break