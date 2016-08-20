from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

'''
This is an example showing how to create an export file from
an existing chat bot that can then be used to train other bots.
'''

chatbot = ChatBot("Export Example Bot")

# First, lets train our bot with some data
chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("chatterbot.corpus.english")

# Now we can export the data to a file
chatbot.trainer.export_for_training('./myfile.json')
