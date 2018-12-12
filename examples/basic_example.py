from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new chat bot named Charlie
chatbot = ChatBot('Charlie')

# Create a new trainer for the chatbox
trainer = ChatterBotCorpusTrainer(chatbot.storage)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english");

# Get a response to the input text 'I would like to book a flight.'
response = chatbot.get_response('I would like to book a flight.')

print(response)
