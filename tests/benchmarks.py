"""
Run this file to generate benchmark data for various
chat bot configurations.
"""

import time
import string
import random
from chatterbot import ChatBot
from pymongo.errors import ServerSelectionTimeoutError
from pymongo import MongoClient


BASE_CONFIGURATION = {
    'trainer': 'chatterbot.trainers.ListTrainer'
}

CONFIGURATIONS = [
    {
        'description': 'Test the levenshtein distance comparison algorithm and file storage',
        'logic_adapters': [
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
                'response_selection_method': 'chatterbot.response_selection.get_first_response'
            }
        ],
        'storage_adapter': {
            'import_path': 'chatterbot.storage.JsonFileStorageAdapter',
            'silence_performance_warning': True
        },
    },
    {
        'description': 'Test the synset distance comparison algorithm and file storage',
        'logic_adapters': [
            {
                'import_path': 'chatterbot.logic.BestMatch',
                'statement_comparison_function': 'chatterbot.comparisons.synset_distance',
                'response_selection_method': 'chatterbot.response_selection.get_first_response'
            }
        ],
        'storage_adapter': {
            'import_path': 'chatterbot.storage.JsonFileStorageAdapter',
            'silence_performance_warning': True
        },
    }
]

# Skip these tests if a mongo client is not running
try:
    client = MongoClient(
        serverSelectionTimeoutMS=0.01
    )
    client.server_info()

    CONFIGURATIONS.extend([
        {
            'description': 'Test the levenshtein distance comparison algorithm and Mongo DB storage',
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'statement_comparison_function': 'chatterbot.comparisons.levenshtein_distance',
                    'response_selection_method': 'chatterbot.response_selection.get_first_response'
                }
            ],
            'storage_adapter': 'chatterbot.storage.MongoDatabaseAdapter'
        },
        {
            'description': 'Test the synset distance comparison algorithm and Mongo DB storage',
            'logic_adapters': [
                {
                    'import_path': 'chatterbot.logic.BestMatch',
                    'statement_comparison_function': 'chatterbot.comparisons.synset_distance',
                    'response_selection_method': 'chatterbot.response_selection.get_first_response'
                }
            ],
            'storage_adapter': 'chatterbot.storage.MongoDatabaseAdapter'
        }
    ])

except ServerSelectionTimeoutError:
    print('Not running Mongo DB benchmarking')


def generate_strings(total_strings, string_length=20):
    """
    Generate a list of random strings.
    """
    statements = []
    for _ in range(0, total_strings):
        text = ''.join(
            random.choice(string.ascii_letters + string.digits + ' ') for _ in range(string_length)
        )
        statements.append(text)
    return statements


STATEMENT_LIST = generate_strings(10)

for config in CONFIGURATIONS:
    configuration = BASE_CONFIGURATION.copy()
    configuration.update(config)

    chatbot = ChatBot('Benchmark', **configuration)
    chatbot.train(STATEMENT_LIST)

    start_time = time.time()

    chatbot.get_response('Hello')

    durration = time.time() - start_time

    print(configuration['description'])
    print('Durration was {} seconds'.format(durration))
