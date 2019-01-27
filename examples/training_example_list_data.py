from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer


'''
This is an example showing how to train a chat bot using the
ChatterBot ListTrainer.
'''

chatbot = ChatBot('Example Bot')

# Start by training our bot with the ChatterBot corpus data
trainer = ListTrainer(chatbot)

trainer.train([
    'Hello, how are you?',
    'I am doing well.',
    'That is good to hear.',
    'Thank you'
])

# You can train with a second list of data to add response variations

trainer.train([
    'Hello, how are you?',
    'I am great.',
    'That is awesome.',
    'Thanks'
])

# Now let's get a response to a greeting
response = chatbot.get_response('How are you doing today?')
print(response)
