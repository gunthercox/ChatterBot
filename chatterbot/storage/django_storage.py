from chatterbot.storage import StorageAdapter
from chatterbot import constants


class DjangoStorageAdapter(StorageAdapter):
    """
    Storage adapter that allows ChatterBot to interact with
    Django storage backends.

    :param database: The Django database alias to use (default: 'default')
    :type database: str
    :param statement_model: The Statement model to use (default: reads from CHATTERBOT_STATEMENT_MODEL setting)
    :type statement_model: str
    :param tag_model: The Tag model to use (default: reads from CHATTERBOT_TAG_MODEL setting)
    :type tag_model: str
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from django.conf import settings

        self.django_app_name = kwargs.get(
            'django_app_name',
            constants.DEFAULT_DJANGO_APP_NAME
        )

        self.database = kwargs.get('database', 'default')

        # Support custom models via kwargs or Django settings
        self.statement_model = kwargs.get(
            'statement_model',
            getattr(
                settings,
                'CHATTERBOT_STATEMENT_MODEL',
                f'{self.django_app_name}.Statement'
            )
        )

        self.tag_model = kwargs.get(
            'tag_model',
            getattr(
                settings,
                'CHATTERBOT_TAG_MODEL',
                f'{self.django_app_name}.Tag'
            )
        )

    def get_statement_model(self):
        from django.apps import apps
        return apps.get_model(self.statement_model)

    def get_tag_model(self):
        from django.apps import apps
        return apps.get_model(self.tag_model)

    def count(self) -> int:
        Statement = self.get_model('statement')
        return Statement.objects.using(self.database).count()

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from django.db.models import Q

        Statement = self.get_model('statement')

        kwargs.pop('page_size', 1000)
        order_by = kwargs.pop('order_by', None)
        tags = kwargs.pop('tags', [])
        exclude_text = kwargs.pop('exclude_text', None)
        exclude_text_words = kwargs.pop('exclude_text_words', [])
        persona_not_startswith = kwargs.pop('persona_not_startswith', None)
        search_text_contains = kwargs.pop('search_text_contains', None)
        search_in_response_to_contains = kwargs.pop('search_in_response_to_contains', None)

        # Convert a single sting into a list if only one tag is provided
        if isinstance(tags, str):
            tags = [tags]

        if tags:
            kwargs['tags__name__in'] = tags

        statements = Statement.objects.using(self.database).filter(**kwargs)

        if exclude_text:
            statements = statements.exclude(
                text__in=exclude_text
            )

        if exclude_text_words:
            or_query = [
                ~Q(text__icontains=word) for word in exclude_text_words
            ]

            statements = statements.filter(
                *or_query
            )

        if persona_not_startswith:
            statements = statements.exclude(
                persona__startswith='bot:'
            )

        if search_text_contains:
            or_query = Q()

            for word in search_text_contains.split(' '):
                or_query |= Q(search_text__contains=word)

            statements = statements.filter(
                or_query
            )

        if search_in_response_to_contains:
            or_query = Q()

            for word in search_in_response_to_contains.split(' '):
                or_query |= Q(search_in_response_to__contains=word)

            statements = statements.filter(
                or_query
            )

        if order_by:
            statements = statements.order_by(*order_by)

        for statement in statements.iterator():
            yield statement

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        tags = kwargs.pop('tags', [])

        if 'search_in_response_to' in kwargs and kwargs['search_in_response_to'] is None:
            kwargs['search_in_response_to'] = ''

        statement = Statement(**kwargs)

        statement.save(using=self.database)

        tags_to_add = []

        for _tag in tags:
            tag, _ = Tag.objects.using(self.database).get_or_create(name=_tag)
            tags_to_add.append(tag)

        statement.tags.add(*tags_to_add)

        return statement

    def create_many(self, statements):
        """
        Creates multiple statement entries.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        tag_cache = {}

        for statement in statements:

            statement_data = statement.serialize()
            tag_data = statement_data.pop('tags', [])

            statement_model_object = Statement(**statement_data)

            statement_model_object.save(using=self.database)

            tags_to_add = []

            for tag_name in tag_data:
                if tag_name in tag_cache:
                    tag = tag_cache[tag_name]
                else:
                    tag, _ = Tag.objects.using(self.database).get_or_create(name=tag_name)
                    tag_cache[tag_name] = tag
                tags_to_add.append(tag)

            statement_model_object.tags.add(*tags_to_add)

    def update(self, statement):
        """
        Update the provided statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        if hasattr(statement, 'id'):
            statement.save(using=self.database)
        else:
            statement = Statement.objects.using(self.database).create(
                text=statement.text,
                search_text=statement.search_text,
                conversation=statement.conversation,
                in_response_to=statement.in_response_to,
                search_in_response_to=statement.search_in_response_to or '',
                created_at=statement.created_at
            )

        for _tag in statement.tags.all():
            tag, _ = Tag.objects.using(self.database).get_or_create(name=_tag)

            statement.tags.add(tag)

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        Statement = self.get_model('statement')

        statement = Statement.objects.using(self.database).order_by('?').first()

        if statement is None:
            raise self.EmptyDatabaseException()

        return statement

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        Statement = self.get_model('statement')

        statements = Statement.objects.using(self.database).filter(text=statement_text)

        statements.delete()

    def drop(self):
        """
        Remove all data from the database.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        Statement.objects.using(self.database).all().delete()
        Tag.objects.using(self.database).all().delete()
