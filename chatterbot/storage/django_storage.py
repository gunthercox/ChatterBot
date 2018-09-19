from chatterbot.storage import StorageAdapter
from chatterbot import constants


class DjangoStorageAdapter(StorageAdapter):
    """
    Storage adapter that allows ChatterBot to interact with
    Django storage backends.
    """

    def __init__(self, **kwargs):
        super(DjangoStorageAdapter, self).__init__(**kwargs)

        self.adapter_supports_queries = False
        self.django_app_name = kwargs.get(
            'django_app_name',
            constants.DEFAULT_DJANGO_APP_NAME
        )

    def get_statement_model(self):
        from django.apps import apps
        return apps.get_model(self.django_app_name, 'Statement')

    def get_tag_model(self):
        from django.apps import apps
        return apps.get_model(self.django_app_name, 'Tag')

    def count(self):
        Statement = self.get_model('statement')
        return Statement.objects.count()

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        Statement = self.get_model('statement')

        order_by = kwargs.pop('order_by', None)

        statements = Statement.objects.filter(**kwargs)

        if order_by:
            statements = statements.order_by(*order_by)

        return statements

    def create(self, **kwargs):
        """
        Creates a new statement matching the keyword arguments specified.
        Returns the created statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        tags = kwargs.pop('tags', [])

        statement = Statement(**kwargs)

        statement.save()

        for _tag in tags:
            tag, _ = Tag.objects.get_or_create(name=_tag)

            statement.tags.add(tag)

        return statement

    def update(self, statement):
        """
        Update the provided statement.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        if hasattr(statement, 'id'):
            statement.save()
        else:
            statement = Statement.objects.create(
                text=statement.text,
                conversation=statement.conversation,
                in_response_to=statement.in_response_to,
                created_at=statement.created_at
            )

        for _tag in statement.tags.all():
            tag, _ = Tag.objects.get_or_create(name=_tag)

            statement.tags.add(tag)

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        Statement = self.get_model('statement')
        return Statement.objects.order_by('?').first()

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        Statement = self.get_model('statement')

        statements = Statement.objects.filter(text=statement_text)

        statements.delete()

    def drop(self):
        """
        Remove all data from the database.
        """
        Statement = self.get_model('statement')
        Tag = self.get_model('tag')

        Statement.objects.all().delete()
        Tag.objects.all().delete()

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        """
        Statement = self.get_model('statement')

        statements_with_responses = Statement.objects.filter(
            in_response_to__isnull=False
        ).values_list('in_response_to', flat=True)

        return Statement.objects.filter(text__in=statements_with_responses)
