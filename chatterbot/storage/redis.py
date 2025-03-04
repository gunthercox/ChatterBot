from datetime import datetime
from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Statement as StatementObject


def _escape_redis_special_characters(text):
    """
    Escape special characters in a string that are used in redis queries.
    """
    # https://stackoverflow.com/questions/65718424/redis-escape-special-character
    # TODO
    return text.replace(':', '\\:')


class RedisVectorStorageAdapter(StorageAdapter):
    """
    .. note:: BETA feature: this storage adapter is new and experimental.
              Its functionality and default parameters might change in the future.

    The RedisVectorStorageAdapter allows ChatterBot to store conversation
    data in a redis instance.

    All parameters are optional, by default a redis instance on localhost is assumed.

    :keyword database_uri: eg: redis://localhost:6379/0',
        The database_uri can be specified to choose a redis instance.
    :type database_uri: str
    """

    class RedisMetaDataType:
        """
        Subclass for redis config metadata type enumerator.
        """
        TAG = 'tag'
        TEXT = 'text'
        NUMERIC = 'numeric'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from langchain_redis import RedisVectorStore, RedisConfig
        from langchain_huggingface import HuggingFaceEmbeddings

        self.database_uri = kwargs.get('database_uri', 'redis://localhost:6379/0')

        config = RedisConfig(
            index_name='chatterbot',
            redis_url=self.database_uri,
            metadata_schema=[
                {
                    'name': 'conversation',
                    'type': self.RedisMetaDataType.TAG,
                },
                {
                    'name': 'in_response_to',
                    'type': self.RedisMetaDataType.TEXT,
                },
                {
                    'name': 'created_at',
                    'type': self.RedisMetaDataType.NUMERIC,
                },
                {
                    'name': 'persona',
                    'type': self.RedisMetaDataType.TEXT,
                },
                {
                    'name': 'tags',
                    'type': self.RedisMetaDataType.TAG,
                    # 'separator': '|'
                },
            ],
        )

        # from_existing_index?

        self.logger.info('Loading HuggingFace embeddings')

        # TODO: Research different embeddings
        # https://python.langchain.com/docs/integrations/vectorstores/mongodb_atlas/#initialization

        embeddings = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-mpnet-base-v2'
        )

        self.logger.info('Creating Redis Vector Store')

        self.vector_store = RedisVectorStore(embeddings, config=config)

    def get_statement_model(self):
        """
        Return the statement model.
        """
        from langchain_core.documents import Document

        return Document

    def model_to_object(self, document):
        values = {
            'text': document.page_content,
        }

        if document.id:
            values['id'] = document.id

        values.update(document.metadata)

        # If the value is an empty string, set it to None
        # Metadata values are stored as strings and cannot be null
        if values['in_response_to'] == '':
            values['in_response_to'] = None

        tags = values['tags']
        values['tags'] = list(set(tags.split('|') if tags else []))

        return StatementObject(**values)

    def count(self):
        """
        Return the number of entries in the database.
        """

        '''
        faiss_vector_store = FAISS(
            embedding_function=embedding_function,
            index=IndexFlatL2(embedding_size),
            docstore=InMemoryDocstore(),
            index_to_docstore_id={}
        )
        doc_count = faiss_vector_store.index.ntotal
        '''

        client = self.vector_store.index.client
        return client.dbsize()

    def remove(self, statement):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        self.vector_store.delete(ids=[statement.id.split(':')[1]])

    def filter(self, page_size=4, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain all
        listed attributes and in which all values match
        for all listed attributes will be returned.

        kwargs:
            - conversation
            - persona
            - tags
            - in_response_to
            - text
            - exclude_text
            - exclude_text_words
            - persona_not_startswith
            - search_text_contains
            - order_by
        """
        from redisvl.query.filter import Tag, Text

        # https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/query_syntax/
        filter_condition = None

        if 'in_response_to' in kwargs:
            filter_condition = Text('in_response_to') == kwargs['in_response_to']

        if 'conversation' in kwargs:
            query = Tag('conversation') == kwargs['conversation']
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'persona' in kwargs:
            query = Tag('persona') == kwargs['persona']
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'tags' in kwargs:
            query = Tag('tags') == kwargs['tags']
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'exclude_text' in kwargs:
            query = Text('text') != '|'.join([
                f'%%{text}%%' for text in kwargs['exclude_text']
            ])
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'exclude_text_words' in kwargs:
            _query = '|'.join([
                f'%%{text}%%' for text in kwargs['exclude_text_words']
            ])
            query = Text('text') % f'-({ _query })'
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'persona_not_startswith' in kwargs:
            _query = kwargs['persona_not_startswith'].replace(':', '\\:')
            query = Text('persona') % f'-(%%{_query}%%)'
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'search_text_contains' in kwargs:
            # TODO: Maybe the usage here is a bit different
            # since `text` is already doing a similarity search
            # ^ Maybe swap them, so search text is the main search
            # and text is an == search?
            # TODO: The `search_text` value also won't be generated during training
            _query = kwargs["search_text_contains"].replace('!', '\\!')  # TODO: Escape special characters
            query = Text('text') % '|'.join([f'%%{_q}%%' for _q in _query.split()])
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        text = kwargs.get('text', '')

        ordering = kwargs.get('order_by', None)

        if ordering:
            ordering = ','.join(ordering)

        # similarity_search_with_score
        documents = self.vector_store.similarity_search(
            text,
            k=page_size,  # The number of results to return
            return_all=True,  # Include the full document with IDs
            filter=filter_condition,
            sort_by=ordering
        )

        return [self.model_to_object(document) for document in documents]

    def create(
        self,
        text,
        in_response_to=None,
        tags=None,
        **kwargs
    ):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        # from langchain_community.vectorstores.redis.constants import REDIS_TAG_SEPARATOR

        _default_date = datetime.now()

        metadata = {
            'category': kwargs.get('category', ''),
            'in_response_to': in_response_to or '',
            # NOTE: `created_at` must have a valid numeric value or results will
            # not be returned for similarity_search for some reason
            'created_at': kwargs.get('created_at') or int(_default_date.strftime('%y%m%d')),
            'tags': '|'.join(tags) if tags else '',
            'conversation': kwargs.get('conversation', ''),
            'persona': kwargs.get('persona', ''),
        }

        ids = self.vector_store.add_texts([text], [metadata])

        metadata['created_at'] = _default_date
        metadata['tags'] = tags or []
        statement = StatementObject(
            id=ids[0],
            text=text,
            **metadata
        )
        return statement

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        Document = self.get_statement_model()
        documents = [
            Document(
                page_content=statement.text,
                metadata={
                    'conversation': statement.conversation or '',
                    'in_response_to': statement.in_response_to or '',
                    'created_at': int(statement.created_at.strftime('%y%m%d')),
                    'persona': statement.persona or '',
                    'tags': '|'.join(statement.tags) if statement.tags else '',
                }
            ) for statement in statements
        ]

        self.logger.info('Adding documents to the vector store')

        self.vector_store.add_documents(documents)

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        metadata = {
            'conversation': statement.conversation or '',
            'in_response_to': statement.in_response_to or '',
            'created_at': int(statement.created_at.strftime('%y%m%d')),
            'persona': statement.persona or '',
            'tags': '|'.join(statement.tags) if statement.tags else '',
        }

        Document = self.get_statement_model()
        document = Document(
            page_content=statement.text,
            metadata=metadata,
        )

        if statement.id:
            self.vector_store.add_texts([statement.text], [metadata], keys=[statement.id.split(':')[1]])
        else:
            self.vector_store.add_documents([document])

    def get_random(self):
        """
        Returns a random statement from the database.
        """
        client = self.vector_store.index.client

        random_key = client.randomkey()

        if random_key:
            random_id = random_key.decode().split(':')[1]

            documents = self.vector_store.get_by_ids([random_id])

            if documents:
                return self.model_to_object(documents[0])
        
        raise self.EmptyDatabaseException()

    def drop(self):
        """
        Remove all existing documents from the database.
        """
        index_name = self.vector_store.config.index_name
        client = self.vector_store.index.client

        for key in client.scan_iter(f'{index_name}:*'):
            # self.vector_store.index.drop_keys(key)
            client.delete(key)

        # Commenting this out for now because there is no step
        # to recreate the index after it is dropped (really what
        # we want is to delete all the keys in the index, but
        # keep the index itself)
        # self.vector_store.index.delete(drop=True)
