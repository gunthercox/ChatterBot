import random
from chatterbot.storage import StorageAdapter


class SQLStorageAdapter(StorageAdapter):
    """
    The SQLStorageAdapter allows ChatterBot to store conversation
    data in any database supported by the SQL Alchemy ORM.

    All parameters are optional, by default a sqlite database is used.

    It will check if tables are present, if they are not, it will attempt
    to create the required tables.

    :keyword database_uri: eg: sqlite:///database_test.sqlite3',
        The database_uri can be specified to choose database driver.
    :type database_uri: str
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        from sqlalchemy import create_engine, inspect, event
        from sqlalchemy import Index
        from sqlalchemy.engine import Engine
        from sqlalchemy.orm import sessionmaker

        self.database_uri = kwargs.get('database_uri', False)

        # None results in a sqlite in-memory database as the default
        if self.database_uri is None:
            self.database_uri = 'sqlite://'

        # Create a file database if the database is not a connection string
        if not self.database_uri:
            self.database_uri = 'sqlite:///db.sqlite3'

        self.engine = create_engine(self.database_uri)

        if self.database_uri.startswith('sqlite://'):

            @event.listens_for(Engine, 'connect')
            def set_sqlite_pragma(dbapi_connection, connection_record):
                dbapi_connection.execute('PRAGMA journal_mode=WAL')
                dbapi_connection.execute('PRAGMA synchronous=NORMAL')

        if not inspect(self.engine).has_table('statement'):
            self.create_database()

        # Check if the expected index exists on the text field of the statement table
        if not inspect(self.engine).has_index('statement', 'idx_cb_search_text'):
            from chatterbot.ext.sqlalchemy_app.models import Statement

            search_text_index = Index(
                'idx_cb_search_text',
                Statement.search_text
            )

            search_text_index.create(bind=self.engine)

        # Check if the expected index exists on the in_response_to field of the statement table
        if not inspect(self.engine).has_index('statement', 'idx_cb_search_in_response_to'):
            from chatterbot.ext.sqlalchemy_app.models import Statement

            search_in_response_to_index = Index(
                'idx_cb_search_in_response_to',
                Statement.search_in_response_to
            )

            search_in_response_to_index.create(bind=self.engine)

        self.Session = sessionmaker(bind=self.engine, expire_on_commit=True)

    def get_statement_model(self):
        """
        Return the statement model.
        """
        from chatterbot.ext.sqlalchemy_app.models import Statement
        return Statement

    def get_tag_model(self):
        """
        Return the conversation model.
        """
        from chatterbot.ext.sqlalchemy_app.models import Tag
        return Tag

    def model_to_object(self, statement):
        from chatterbot.conversation import Statement as StatementObject

        return StatementObject(**statement.serialize())

    def count(self) -> int:
        """
        Return the number of entries in the database.
        """
        Statement = self.get_model('statement')

        session = self.Session()
        statement_count = session.query(Statement).count()
        session.close()
        return statement_count

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements where the response text matches
        the input text.
        """
        Statement = self.get_model('statement')
        session = self.Session()

        query = session.query(Statement).filter_by(text=statement_text)
        record = query.first()

        session.delete(record)
        session.commit()
        session.close()

    def filter(self, **kwargs):
        """
        Returns a list of objects from the database.
        The kwargs parameter can contain any number
        of attributes. Only objects which contain all
        listed attributes and in which all values match
        for all listed attributes will be returned.
        """
        from sqlalchemy import or_

        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        page_size = kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)
        search_in_response_to_contains = kwargs.pop('search_in_response_to_contains', None)

        # Convert a single sting into a list if only one tag is provided
        if type(tags) == str:
            tags = [tags]

        if len(kwargs) == 0:
            statements = session.query(Statement).filter()
        else:
            statements = session.query(Statement).filter_by(**kwargs)

        if tags:
            statements = statements.join(Statement.tags).filter(
                Tag.name.in_(tags)
            )

        if exclude_text:
            statements = statements.filter(
                ~Statement.text.in_(exclude_text)
            )

        if exclude_text_words:
            or_word_query = [
                Statement.text.ilike('%' + word + '%') for word in exclude_text_words
            ]
            statements = statements.filter(
                ~or_(*or_word_query)
            )

        if persona_not_startswith:
            statements = statements.filter(
                ~Statement.persona.startswith('bot:')
            )

        if search_text_contains:
            or_query = [
                Statement.search_text.contains(word) for word in search_text_contains.split(' ')
            ]
            statements = statements.filter(
                or_(*or_query)
            )

        if search_in_response_to_contains:
            or_query = [
                Statement.search_in_response_to.contains(word) for word in search_in_response_to_contains.split(' ')
            ]
            statements = statements.filter(
                or_(*or_query)
            )

        if order_by:

            if 'created_at' in order_by:
                index = order_by.index('created_at')
                order_by[index] = Statement.created_at.asc()

            statements = statements.order_by(*order_by)

        total_statements = statements.count()

        for start_index in range(0, total_statements, page_size):
            for statement in statements.slice(start_index, start_index + page_size):
                yield self.model_to_object(statement)

        session.close()

    def create(
        self,
        text,
        in_response_to=None,
        tags=None,
        search_text=None,
        search_in_response_to=None,
        **kwargs
    ):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        if search_text is None:
            if self.raise_on_missing_search_text:
                raise Exception('generate a search_text value')

        if search_in_response_to is None and in_response_to is not None:
            if self.raise_on_missing_search_text:
                raise Exception('generate a search_in_response_to value')

        statement = Statement(
            text=text,
            in_response_to=in_response_to,
            search_text=search_text,
            search_in_response_to=search_in_response_to,
            **kwargs
        )

        tags = frozenset(tags) if tags else frozenset()
        for tag_name in frozenset(tags):
            # TODO: Query existing tags in bulk
            tag = session.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                # Create the tag
                tag = Tag(name=tag_name)

            statement.tags.append(tag)

        session.add(statement)

        session.commit()

        session.refresh(statement)

        statement_object = self.model_to_object(statement)

        session.close()

        return statement_object

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        create_statements = []
        create_tags = {}

        # Check if any statements already have a search text
        have_search_text = any(statement.search_text for statement in statements)

        # Generate search text values in bulk
        if not have_search_text:
            if self.raise_on_missing_search_text:
                raise Exception('generate bulk_search_text values')

        for statement in statements:

            statement_data = statement.serialize()
            tag_data = statement_data.pop('tags', [])

            statement_model_object = Statement(**statement_data)

            new_tags = set(tag_data) - set(create_tags.keys())

            if new_tags:
                existing_tags = session.query(Tag).filter(
                    Tag.name.in_(new_tags)
                )

                for existing_tag in existing_tags:
                    create_tags[existing_tag.name] = existing_tag

            for tag_name in tag_data:
                if tag_name in create_tags:
                    tag = create_tags[tag_name]
                else:
                    # Create the tag if it does not exist
                    tag = Tag(name=tag_name)

                    create_tags[tag_name] = tag

                statement_model_object.tags.append(tag)
            create_statements.append(statement_model_object)

        session.add_all(create_statements)
        session.commit()

    def update(self, statement):
        """
        Modifies an entry in the database.
        Creates an entry if one does not exist.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()
        record = None

        if hasattr(statement, 'id') and statement.id is not None:
            record = session.get(Statement, statement.id)
        else:
            record = session.query(Statement).filter(
                Statement.text == statement.text,
                Statement.conversation == statement.conversation,
            ).first()

            # Create a new statement entry if one does not already exist
            if not record:
                record = Statement(
                    text=statement.text,
                    conversation=statement.conversation,
                    persona=statement.persona
                )

        # Update the response value
        record.in_response_to = statement.in_response_to

        record.created_at = statement.created_at

        if not statement.search_text:
            if self.raise_on_missing_search_text:
                raise Exception('update issued without search_text value')

        if statement.in_response_to and not statement.search_in_response_to:
            if self.raise_on_missing_search_text:
                raise Exception('update issued without search_in_response_to value')

        for tag_name in statement.get_tags():
            tag = session.query(Tag).filter_by(name=tag_name).first()

            if not tag:
                # Create the record
                tag = Tag(name=tag_name)

            record.tags.append(tag)

        session.add(record)
        session.commit()
        session.close()

    def get_random(self):
        """
        Returns a random statement from the database.
        """
        Statement = self.get_model('statement')

        session = self.Session()
        count = self.count()
        if count < 1:
            raise self.EmptyDatabaseException()

        random_index = random.randrange(0, count)
        random_statement = session.query(Statement)[random_index]

        statement = self.model_to_object(random_statement)

        session.close()
        return statement

    def drop(self):
        """
        Drop the database.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        session = self.Session()

        session.query(Statement).delete()
        session.query(Tag).delete()

        session.commit()
        session.close()

    def create_database(self):
        """
        Populate the database with the tables.
        """
        from chatterbot.ext.sqlalchemy_app.models import Base
        Base.metadata.create_all(self.engine)
