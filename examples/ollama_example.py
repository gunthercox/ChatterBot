"""
Example of using Ollama LLM with MCP tool support via OllamaLogicAdapter.

This example shows how to integrate Ollama models into ChatterBot's consensus
voting system and optionally enable tool calling for specialized tasks.
"""
from chatterbot import ChatBot


# Create a new instance of a ChatBot
bot = ChatBot(
    'Ollama Example Bot',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.OllamaLogicAdapter',
            'model': 'llama3.1',
            'host': 'http://localhost:11434',
            # Optionally enable tools
            # 'logic_adapters_as_tools': [
            #     'chatterbot.logic.MathematicalEvaluation',
            #     'chatterbot.logic.TimeLogicAdapter',
            # ]
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
