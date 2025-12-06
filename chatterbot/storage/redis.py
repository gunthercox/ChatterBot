from datetime import datetime
import json
import re
from chatterbot.storage import StorageAdapter
from chatterbot.conversation import Statement as StatementObject


def _escape_redis_special_characters(text):
    """
    Escape special characters in a string that are used in redis queries.

    This function escapes characters that would interfere with the query syntax
    used in the filter() method, specifically:
    - Pipe (|) which is used as the OR operator when joining search terms
    - Characters that could break the wildcard pattern matching
    """
    from redisvl.query.filter import TokenEscaper

    # Remove space (last character) and add pipe
    escape_pattern = TokenEscaper.DEFAULT_ESCAPED_CHARS.rstrip(' ]') + r'\|]'

    escaper = TokenEscaper(escape_chars_re=re.compile(escape_pattern))
    return escaper.escape(text)


class RedisVectorStorageAdapter(StorageAdapter):
    """
    .. warning:: BETA feature (Released March, 2025): this storage adapter is new
        and experimental. Its functionality and default parameters might change
        in the future and its behavior has not yet been finalized.

    The RedisVectorStorageAdapter allows ChatterBot to store conversation
    data in a redis instance.

    All parameters are optional, by default a redis instance on localhost is assumed.

    :keyword database_uri: eg: redis://localhost:6379/0',
        The database_uri can be specified to choose a redis instance.
    :type database_uri: str

    NOTES:
    * Unlike other database based storage adapters, the RedisVectorStorageAdapter
      does not leverage `search_text` and `search_in_response_to` fields for indexing.
      Instead, it uses vector embeddings to find similar statements based on
      semantic similarity. This allows for more flexible and context-aware matching.
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
        from chatterbot.vectorstores import RedisVectorStore
        from langchain_redis import RedisConfig  # RedisVectorStore
        from langchain_huggingface import HuggingFaceEmbeddings

        self.database_uri = kwargs.get('database_uri', 'redis://localhost:6379/0')

        config = RedisConfig(
            index_name='chatterbot',
            redis_url=self.database_uri,
            content_field='in_response_to',
            metadata_schema=[
                {
                    'name': 'conversation',
                    'type': self.RedisMetaDataType.TAG,
                },
                {
                    'name': 'text',
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

        # TODO should this call from_existing_index if connecting to
        # a redis instance that already contains data?

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

        in_response_to = document.page_content

        # If the value is an empty string, set it to None
        # to match the expected type (the vector store does
        # not use null values)
        if in_response_to == '':
            in_response_to = None

        values = {
            'in_response_to': in_response_to,
        }

        if document.id:
            values['id'] = document.id

        values.update(document.metadata)

        # Convert Unix timestamp back to datetime for StatementObject
        # Redis may return this as int, float, or string representation
        if 'created_at' in values:
            created_at_value = values['created_at']
            if isinstance(created_at_value, str):
                # Convert string to float first
                created_at_value = float(created_at_value)
            if isinstance(created_at_value, (int, float)):
                values['created_at'] = datetime.fromtimestamp(created_at_value)

        tags = values['tags']
        values['tags'] = list(set(tags.split('|') if tags else []))

        return StatementObject(**values)

    def count(self) -> int:
        """
        Return the number of entries in the database.
        """

        '''
        TODO
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
        client = self.vector_store.index.client
        client.delete(statement.id)

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
            - search_in_response_to_contains
            - order_by
        """
        from redisvl.query import VectorQuery
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
            _query = _escape_redis_special_characters(kwargs['persona_not_startswith'])
            query = Text('persona') % f'-(%%{_query}%%)'
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'text' in kwargs:
            _query = _escape_redis_special_characters(kwargs['text'])
            query = Text('text') % '|'.join([f'%%{_q}%%' for _q in _query.split()])
            if filter_condition:
                filter_condition &= query
            else:
                filter_condition = query

        if 'search_text_contains' in kwargs:
            # Find statements whose text (responses) are similar.
            #
            # Use semantic similarity on the search query itself. This finds responses
            # that would be semantically appropriate, even if they don't share exact words.
            #
            # Our vectors are of 'in_response_to' (what was said TO the bot),
            # not 'text' (what the bot said). So we use the query as if it were an input,
            # and find statements that would respond to similar inputs. The result is
            # statements whose context (in_response_to) is similar, which tends to yield
            # similar responses.
            _search_query = kwargs['search_text_contains']

            # Use vector similarity to find statements responding to similar contexts
            embedding = self.vector_store.embeddings.embed_query(_search_query)

            return_fields = [
                'text', 'in_response_to', 'conversation', 'persona', 'tags', 'created_at'
            ]

            query = VectorQuery(
                vector=embedding,
                vector_field_name='embedding',
                return_fields=return_fields,
                num_results=page_size,
                filter_expression=filter_condition
            )

            results = self.vector_store.index.query(query)

            Document = self.get_statement_model()
            documents = []
            for result in results:
                in_response_to = result.get('in_response_to', '')

                created_at_int = int(result.get('created_at', 0))
                if created_at_int:
                    created_at = datetime.strptime(str(created_at_int), '%y%m%d')
                else:
                    created_at = datetime.now()

                metadata = {
                    'text': result.get('text', ''),
                    'conversation': result.get('conversation', ''),
                    'persona': result.get('persona', ''),
                    'tags': result.get('tags', ''),
                    'created_at': created_at,
                }
                doc = Document(
                    page_content=in_response_to,
                    metadata=metadata,
                    id=result['id']
                )
                documents.append(doc)

            return [self.model_to_object(document) for document in documents]

        # Redis uses vector similarity: we search for statements whose actual
        # text field is semantically similar to the text that produced this search_text.
        # This is stored in the closest_match.text field, but BestMatch only passes
        # search_text. Since we can't reverse POS tags to original text (for now),
        # we treat this parameter as a signal to do text-based similarity search.
        #
        # Note: The caller should ideally pass the actual text, but for compatibility
        # we'll work with what we receive. In practice, search_text_contains is the
        # better parameter for this use case.
        if 'search_text' in kwargs:
            # For now, we'll treat search_text as a filter-only parameter
            # and fall through to the regular query_search below.
            # This prevents the broken behavior of embedding POS tags.
            # The proper fix requires BestMatch to pass additional context
            # or use search_text_contains instead.
            pass

        ordering = kwargs.get('order_by', None)

        if ordering:
            ordering = ','.join(ordering)

        if 'search_in_response_to_contains' in kwargs:
            _search_text = kwargs.get('search_in_response_to_contains', '')

            # Get embedding for the search text
            embedding = self.vector_store.embeddings.embed_query(_search_text)

            # Build return fields from metadata schema
            return_fields = [
                'text', 'in_response_to', 'conversation', 'persona', 'tags', 'created_at'
            ]

            # Use direct index query via RedisVL
            # langchain's similarity_search has issues with filters in v0.2.4
            # and may not work properly with existing indexes
            # TODO: Look into similarity_search_with_score implementation
            query = VectorQuery(
                vector=embedding,
                vector_field_name='embedding',
                return_fields=return_fields,
                num_results=page_size,
                filter_expression=filter_condition
            )

            # Execute query
            results = self.vector_store.index.query(query)

            # Convert results to Document objects
            Document = self.get_statement_model()
            documents = []
            for result in results:
                # Extract metadata and content
                in_response_to = result.get('in_response_to', '')

                # Convert Unix timestamp back to datetime
                # Redis returns numeric fields as strings
                created_at_timestamp = result.get('created_at', '0')
                if created_at_timestamp and created_at_timestamp != '0':
                    created_at = datetime.fromtimestamp(float(created_at_timestamp))
                else:
                    created_at = datetime.now()

                metadata = {
                    'text': result.get('text', ''),
                    'conversation': result.get('conversation', ''),
                    'persona': result.get('persona', ''),
                    'tags': result.get('tags', ''),
                    'created_at': created_at,
                }
                doc = Document(
                    page_content=in_response_to,
                    metadata=metadata,
                    id=result['id']
                )
                documents.append(doc)
        else:
            documents = self.vector_store.query_search(
                k=page_size,
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

        # Prevent duplicate tag entries in the database
        unique_tags = list(set(tags)) if tags else []

        metadata = {
            'text': text,
            'category': kwargs.get('category', ''),
            # Store created_at as Unix timestamp with microseconds (float)
            # This provides full datetime precision while maintaining Redis NUMERIC field compatibility
            'created_at': kwargs.get('created_at') or _default_date.timestamp(),
            'tags': '|'.join(unique_tags) if unique_tags else '',
            'conversation': kwargs.get('conversation', ''),
            'persona': kwargs.get('persona', ''),
        }

        ids = self.vector_store.add_texts([in_response_to or ''], [metadata])

        metadata['created_at'] = _default_date
        metadata['tags'] = unique_tags
        metadata.pop('text')
        statement = StatementObject(
            id=ids[0],
            text=text,
            in_response_to=in_response_to,
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
                page_content=statement.in_response_to or '',
                metadata={
                    'text': statement.text,
                    'conversation': statement.conversation or '',
                    'created_at': statement.created_at.timestamp(),
                    'persona': statement.persona or '',
                    # Prevent duplicate tag entries in the database
                    'tags': '|'.join(
                        list(set(statement.tags))
                    ) if statement.tags else '',
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
        # Prevent duplicate tag entries in the database
        unique_tags = list(set(statement.tags)) if statement.tags else []

        metadata = {
            'text': statement.text,
            'conversation': statement.conversation or '',
            'created_at': statement.created_at.timestamp(),
            'persona': statement.persona or '',
            'tags': '|'.join(unique_tags) if unique_tags else '',
        }

        Document = self.get_statement_model()
        document = Document(
            page_content=statement.in_response_to or '',
            metadata=metadata,
        )

        if statement.id:
            # When updating with an existing ID, first delete the old entry
            # to ensure a duplicate entry is not created
            client = self.vector_store.index.client
            client.delete(statement.id)

            # NOTE: langchain-redis has an inconsistency - it uses :: for auto-generated
            # IDs but : (single colon) when keys are explicitly provided
            if '::' in statement.id:
                key = statement.id.split('::', 1)[1]
            elif ':' in statement.id:
                key = statement.id.split(':', 1)[1]
            else:
                # If no delimiter found, use the entire ID as the key
                key = statement.id

            ids = self.vector_store.add_texts(
                [document.page_content], [metadata], keys=[key]
            )

            # Normalize the ID to use :: delimiter (if langchain-redis returned single colon)
            if ids and ':' in ids[0] and '::' not in ids[0]:
                # Replace first occurrence of single colon with double colon
                normalized_id = ids[0].replace(':', '::', 1)
                # Update the key in Redis to use the correct format
                client.rename(ids[0], normalized_id)
        else:
            self.vector_store.add_documents([document])

    def get_random(self):
        """
        Returns a random statement from the database.
        """
        client = self.vector_store.index.client

        random_key = client.randomkey()

        if random_key:
            # Get the hash data from Redis
            data = client.hgetall(random_key)

            if data and b'_metadata_json' in data:
                # Parse the metadata
                metadata = json.loads(data[b'_metadata_json'].decode())

                # Convert created_at from Unix timestamp back to datetime
                if 'created_at' in metadata and isinstance(metadata['created_at'], (int, float)):
                    metadata['created_at'] = datetime.fromtimestamp(metadata['created_at'])

                # Get the in_response_to from the hash
                in_response_to = data.get(b'in_response_to', b'').decode()

                # Create a Document-like object to use with model_to_object
                Document = self.get_statement_model()
                document = Document(
                    page_content=in_response_to if in_response_to else '',
                    metadata=metadata,
                    id=random_key.decode()
                )

                return self.model_to_object(document)

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

    def close(self):
        """
        Close the Redis client connection.
        """
        if hasattr(self, 'vector_store') and hasattr(self.vector_store, 'index'):
            if hasattr(self.vector_store.index, 'client'):
                self.vector_store.index.client.close()
