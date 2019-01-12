from chatterbot import ChatBot


bot = ChatBot(
    'Unit Converter',
    logic_adapters=[
        'chatterbot.logic.UnitConversion',
    ]
)

questions = [
    'How many meters are in a kilometer?',
    'How many meters are in one inch?',
    '0 celsius to fahrenheit',
    'one hour is how many minutes ?'
]

# Prints the convertion given the specific question
for question in questions:
    response = bot.get_response(question)
    print(question + ' -  Response: ' + response.text)
