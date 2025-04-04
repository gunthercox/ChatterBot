"""
EXPERIMENTAL: See https://docs.chatterbot.us/large-language-models/ for more information.
Example of using the Ollama API with the Ollama Python client.
"""
from chatterbot import ChatBot


# Create a new instance of a ChatBot
bot = ChatBot(
    'Ollama Example Bot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.Ollama',
            'model': 'gemma3:1b',
            'host': 'http://localhost:11434'
        }
    ],
    stream=True  # Enable streaming responses
)

print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        user_input = input()

        bot_response = bot.get_response(user_input)

        for part in bot_response:
            print(part, end='', flush=True)
        print()

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
