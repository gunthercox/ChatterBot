import uuid


class ConversationModelMixin(object):

    collection_name = 'conversations'

    pk_field = 'id'
    fields = ('id', )

    def get_last_response_statement(self):
        """
        Return the last statement that was received.
        """
        if self.statements.exists():
            # Return the output statement
            return self.statements.latest('id')
        return None

    def get_last_input_statement(self):
        """
        Return the last response that was given.
        """
        if self.statements.count() > 1:
            # Return the input statement
            return self.statements.all()[-2]
        return None

    def serialize(self):
        statements = []

        for statement in self.statements.all():
            statements.append({'text': statement.text})

        return {
            'id': self.id,
            'statements': statements
        }


class StatementRelatedManager(object):

    def __init__(self, conversation, statements):
        self.statements = statements
        self.conversation = conversation

    def exists(self):
        return len(self.statements) > 0

    def count(self):
        return len(self.statements)

    def first(self):
        return self.statements[0]

    def latest(self, *args):
        return self.statements[-1]

    def all(self):
        return self.statements

    def add(self, statement):
        self.statements.append(statement)
        self.conversation.save()
        


class Conversation(ConversationModelMixin):
    """
    A single chat session.
    """

    objects = None

    def __init__(self, **kwargs):
        # A unique identifier for the chat session
        self.uuid = uuid.uuid1()
        self.id = kwargs.get('id', str(self.uuid))

        statements = kwargs.get('statements', [])
        self.statements = StatementRelatedManager(self, statements)

    def save(self):
        self.objects.storage.update(self)


class ConversationManager(object):
    """
    Object to hold and manage multiple chat sessions.
    """

    def __init__(self, storage):
        self.storage = storage

    def create(self):
        """
        Add a new chat session.
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

