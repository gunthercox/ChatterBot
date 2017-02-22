# -*- coding: utf-8 -*-
from chatterbot import ChatBot


# Create a new instance of a ChatBot.
bot = ChatBot(
    'Other Languages Example Bot',
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatchLang',
            'statement_comparison_function': 'chatterbot.comparisons.synset_distance',
            'language': 'spanish',
            'lang': 'spa'
        }
    ],
    trainer='chatterbot.trainers.ListTrainer'
)

# Train the chat bot with a few responses
bot.train([
            "Hola",
            "Hola",
            "¿Cómo estás?",
            "Estoy bien.",
            "Me da gusto",
            "Sí, lo es.",
            "¿Puedo ayudarte en algo?",
            "Sí, tengo una pregunta.",
            "¿Cuál es tu pregunta?",
            "¿Puedo pedir prestada una taza de azúcar?",
            "Lo siento, pero no tengo ninguna.",
            "Gracias de todas formas.",
            "No hay problema."
])

# Get a response for some unexpected input
response = bot.get_response('¿Cómo estás?')
print(response)
