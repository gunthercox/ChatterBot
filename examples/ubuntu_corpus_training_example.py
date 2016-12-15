from chatterbot import ChatBot
import logging


'''
This is an example showing how to train a chat bot using the
Ubuntu Corpus of conversation dialog.
'''

# Enable info level logging
logging.basicConfig(level=logging.INFO)

chatbot = ChatBot(
    'Example Bot',
    trainer='chatterbot.trainers.UbuntuCorpusTrainer'
)

# Start by training our bot with the Ubuntu corpus data
chatbot.train()

# Now let's get a response to a greeting
response = chatbot.get_response('How are you doing today?')
print(response)