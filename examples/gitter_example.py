from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from settings import GITTER


# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)


'''
To use this example, create a new file called settings.py.
In settings.py define the following:

GITTER = {
    "API_TOKEN": "my-api-token",
    "ROOM": "example_project/test_room"
}
'''


chatbot = ChatBot(
    'GitterBot',
    gitter_room=GITTER['ROOM'],
    gitter_api_token=GITTER['API_TOKEN'],
    gitter_only_respond_to_mentions=False,
    input_adapter='chatterbot.input.Gitter',
    output_adapter='chatterbot.output.Gitter'
)

trainer = ChatterBotCorpusTrainer(chatbot)

trainer.train('chatterbot.corpus.english')

# The following loop will execute each time the user enters input
while True:
    try:
        response = chatbot.get_response('')

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
