from chatterbot import ChatBot
from settings import GITTER


chatbot = ChatBot(
    'GitterBot',
    gitter_room=GITTER['ROOM'],
    gitter_api_token=GITTER['API_TOKEN'],
    input_adapter='chatterbot.adapters.input.Gitter',
    output_adapter='chatterbot.adapters.output.Gitter',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

chatbot.train('chatterbot.corpus.english')

# The following loop will execute each time the user enters input
while True:
    try:
        response = chatbot.get_response(None)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break