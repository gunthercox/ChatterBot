from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot('thirteen')

# Create a new trainer for the chatbot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train("chatterbot.corpus.english")


lineCounter = 1
# 开始对话
while True:
    print(chatbot.get_response(input("(" + str(lineCounter) + ") user:")))
    lineCounter += 1