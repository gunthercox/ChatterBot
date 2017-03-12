# -*- coding: utf-8 -*-
from chatterbot import ChatBot

'''
This is an example showing how to create an export file from
an existing chat bot that can then be used to train other bots.
'''

chatbot = ChatBot(
    'Export Example Bot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

# First, lets train our bot with some data
chatbot.train('chatterbot.corpus.english')

# Now we can export the data to a file
chatbot.trainer.export_for_training('./my_export.json')
