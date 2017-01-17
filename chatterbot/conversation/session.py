import uuid
from chatterbot.queues import ResponseQueue


class ModelMixin(object):
    """
    TODO
    """

    @property
    def name(self):
        """
        Return the name of the class in lowercase characters.
        This will be used for the table or collection name in
        the database.
        """
        return str(self.__class__.__name__).lower() + 's'


class Session(ModelMixin):
    """
    A session is an ordered collection of statements
    that are related to each other.
    """

    objects = None

    def __init__(self):
        # A unique identifier for the chat session
        self.uuid = uuid.uuid1()
        self.id_string = str(self.uuid)
        self.id = str(self.uuid)

        # The last 10 statement inputs and outputs
        self.conversation = ResponseQueue(maxsize=10)

        self.objects = self.objects


class ConversationSessionManager(object):
    """
    Object to hold and manage multiple chat sessions.
    """
    sessions = {}

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
        return self.sessions.get(str(session_id), default)

    def update(self, session_id, conversance):
        """
        Add a conversance to a given session if the session exists.
        """
        session_id = str(session_id)
        if session_id in self.sessions:
            self.sessions[session_id].conversation.append(conversance)


Conversation = Session
