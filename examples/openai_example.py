"""
Example of using OpenAI LLM with MCP tool support via OpenAILogicAdapter.

Requires OPENAI_API_KEY environment variable to be set.

This example shows how to integrate OpenAI models into ChatterBot's consensus
voting system and enable tool calling for specialized tasks.
"""
from chatterbot import ChatBot
from dotenv import load_dotenv

# Load the OPENAI_API_KEY from the .env file
load_dotenv('../.env')

# Create a new instance of a ChatBot
bot = ChatBot(
    'OpenAI Example Bot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.OpenAILogicAdapter',
            'model': 'gpt-4o-mini',
            # Enable tools for math, time, and unit conversion
            'logic_adapters_as_tools': [
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter',
                'chatterbot.logic.UnitConversion'
            ]
        }
    ]
)

print('Type something to begin...')

# The following loop will execute each time the user enters input
while True:
    try:
        user_input = input()

        bot_response = bot.get_response(user_input)
        print(bot_response)

    # Press ctrl-c or ctrl-d on the keyboard to exit
    except (KeyboardInterrupt, EOFError, SystemExit):
        break
