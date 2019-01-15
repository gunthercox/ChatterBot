from chatterbot import ChatBot
from chatterbot.conversation import Statement


chatbot = ChatBot(
    'Example Bot',
    # This database will be a temporary in-memory database
    database_uri=None
)

label_a_statements = [
    Statement(text='Hello', tags=['label_a']),
    Statement(text='Hi', tags=['label_a']),
    Statement(text='How are you?', tags=['label_a'])
]

label_b_statements = [
    Statement(text='I like dogs.', tags=['label_b']),
    Statement(text='I like cats.', tags=['label_b']),
    Statement(text='I like animals.', tags=['label_b'])
]

chatbot.storage.create_many(
    label_a_statements + label_b_statements
)

# Return a response from "label_a_statements"
response_from_label_a = chatbot.get_response(
    'How are you?',
    additional_response_selection_parameters={
        'tags': ['label_a']
    }
)

# Return a response from "label_b_statements"
response_from_label_b = chatbot.get_response(
    'How are you?',
    additional_response_selection_parameters={
        'tags': ['label_b']
    }
)

print('Response from label_a collection:', response_from_label_a.text)
print('Response from label_b collection:', response_from_label_b.text)
