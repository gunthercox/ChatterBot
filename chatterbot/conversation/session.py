import uuid


class Session(object):
    """
    A session is an ordered collection of statements
    that are related to each other.
    """

    objects = None
    collection_name = 'conversations'

    pk_field = 'id'
    fields = (id, )

    def __init__(self, **kwargs):
        # A unique identifier for the chat session
        self.uuid = uuid.uuid1()
        self.id = kwargs.get('id', str(self.uuid))

        # The last 10 statement inputs and outputs
        self.conversation = kwargs.get('conversation', [])

    def get_last_response_statement(self):
        """
        Return the last statement that was received.
        """
        if self.conversation:
            # Return the output statement
            return self.conversation[-1]
        return None

    def get_last_input_statement(self):
        """
        Return the last response that was given.
        """
        if len(self.conversation) > 1:
            # Return the input statement
            return self.conversation[-2]
        return None

    def serialize(self):
        statements = []

        for statement in self.conversation:
            statements.append({'text': statement.text})

        return {
            'id': self.id,
            'conversation': statements
        }


class ConversationSessionManager(object):
    """
    Object to hold and manage multiple chat sessions.
    """

    def __init__(self, storage):
        self.storage = storage

    def create(self):
        """
        Create a new conversation.
        """
        conversation = self.storage.Conversation()
        conversation.save()
        return conversation

    def get(self, session_id, default=None):
        """
        Return a session given a unique identifier.
        """
        results = self.storage.filter(self.storage.Conversation, id=session_id)
        if results:
            return results[0]
        else:
            return default

    def update(self, session_id, conversance):
        """
        Add a conversance to a given session if the session exists.
        """
        results = self.storage.filter(self.storage.Conversation, id=session_id)

        # If the conversation exists
        if results:
            session = results[0]
            session.conversation.append(conversance)
            self.storage.update(session)


Conversation = Session
