"""
EXPERIMENTAL: See https://docs.chatterbot.us/large-language-models/ for more information.
Example of using the OpenAI API with the OpenAI Python client.
"""
from chatterbot import ChatBot
from dotenv import load_dotenv

# Load the OPENAI_API_KEY from the .env file
load_dotenv('../.env')

# Create a new instance of a ChatBot
bot = ChatBot(
    'OpenAI Example Bot',
    model={
        'client': 'chatterbot.llm.OpenAI',
        'model': 'gpt-4o-mini',
    },
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
