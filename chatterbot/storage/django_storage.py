from chatterbot.storage import StorageAdapter


class DjangoStorageAdapter(StorageAdapter):
    """
    Storage adapter that allows ChatterBot to interact with
    Django storage backends.
    """

    def __init__(self, **kwargs):
        super(DjangoStorageAdapter, self).__init__(**kwargs)

        self.adapter_supports_queries = False
        self.django_app_name = kwargs.get('django_app_name', 'django_chatterbot')

    def count(self):
        from django.apps import apps
        Statement = apps.get_model(self.django_app_name, 'Statement')
        return Statement.objects.count()

    def find(self, statement_text):
        from django.apps import apps
        Statement = apps.get_model(self.django_app_name, 'Statement')
        try:
            return Statement.objects.get(text=statement_text)
        except Statement.DoesNotExist as e:
            self.logger.info(str(e))
            return None

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from django.apps import apps
        Statement = apps.get_model(self.django_app_name, 'Statement')
        from django.db.models import Q

        order = kwargs.pop('order_by', None)

        RESPONSE_CONTAINS = 'in_response_to__contains'

        if RESPONSE_CONTAINS in kwargs:
            value = kwargs[RESPONSE_CONTAINS]
            del kwargs[RESPONSE_CONTAINS]
            kwargs['in_response__response__text'] = value

        kwargs_copy = kwargs.copy()

        for kwarg in kwargs_copy:
            value = kwargs[kwarg]
            del kwargs[kwarg]
            kwarg = kwarg.replace('in_response_to', 'in_response')
            kwargs[kwarg] = value

        if 'in_response' in kwargs:
            responses = kwargs['in_response']
            del kwargs['in_response']

            if responses:
                kwargs['in_response__response__text__in'] = []
                for response in responses:
                    kwargs['in_response__response__text__in'].append(response)
            else:
                kwargs['in_response'] = None

        parameters = {}
        if 'in_response__response__text' in kwargs:
            value = kwargs['in_response__response__text']
            parameters['responses__statement__text'] = value

        statements = Statement.objects.filter(Q(**kwargs) | Q(**parameters))

        if order:
            statements = statements.order_by(order)

        return statements

    def update(self, statement):
        """
        Update the provided statement.
        """
        from django.apps import apps
        Statement = apps.get_model(self.django_app_name, 'Statement')
        Response = apps.get_model(self.django_app_name, 'Response')

        response_statement_cache = statement.response_statement_cache

        statement, created = Statement.objects.get_or_create(text=statement.text)
        statement.extra_data = getattr(statement, 'extra_data', '')
        statement.save()

        for _response_statement in response_statement_cache:

            response_statement, created = Statement.objects.get_or_create(
                text=_response_statement.text
            )
            response_statement.extra_data = getattr(_response_statement, 'extra_data', '')
            response_statement.save()

            Response.objects.create(
                statement=response_statement,
                response=statement
            )

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from django.apps import apps
        Statement = apps.get_model(self.django_app_name, 'Statement')
        return Statement.objects.order_by('?').first()

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        from django.apps import apps
        from django.db.models import Q

        Statement = apps.get_model(self.django_app_name, 'Statement')
        Response = apps.get_model(self.django_app_name, 'Response')

        statements = Statement.objects.filter(text=statement_text)

        responses = Response.objects.filter(
            Q(statement__text=statement_text) | Q(response__text=statement_text)
        )

        responses.delete()
        statements.delete()

    def get_latest_response(self, conversation_id):
        """
        Returns the latest response in a conversation if it exists.
        Returns None if a matching conversation cannot be found.
        """
        from django.apps import apps

        Response = apps.get_model(self.django_app_name, 'Response')

        response = Response.objects.filter(
            conversations__id=conversation_id
        ).order_by(
            'created_at'
        ).first()

        if not response:
            return None

        return response.response

    def create_conversation(self):
        """
        Create a new conversation.
        """
        from django.apps import apps
        Conversation = apps.get_model(self.django_app_name, 'Conversation')
        conversation = Conversation.objects.create()
        return conversation.id

    def add_to_conversation(self, conversation_id, statement, response):
        """
        Add the statement and response to the conversation.
        """
        from django.apps import apps

        Statement = apps.get_model(self.django_app_name, 'Statement')
        Response = apps.get_model(self.django_app_name, 'Response')

        first_statement = Statement.objects.get(text=statement.text)
        first_response = Statement.objects.get(text=response.text)

        response = Response.objects.create(
            statement=first_statement,
            response=first_response
        )

        response.conversations.add(conversation_id)

    def drop(self):
        """
        Remove all data from the database.
        """
        from django.apps import apps

        Statement = apps.get_model(self.django_app_name, 'Statement')
        Response = apps.get_model(self.django_app_name, 'Response')
        Conversation = apps.get_model(self.django_app_name, 'Conversation')

        Statement.objects.all().delete()
        Response.objects.all().delete()
        Conversation.objects.all().delete()

    def get_response_statements(self):
        """
        Return only statements that are in response to another statement.
        A statement must exist which lists the closest matching statement in the
        in_response_to field. Otherwise, the logic adapter may find a closest
        matching statement that does not have a known response.
        """
        from django.apps import apps
        Statement = apps.get_model(self.django_app_name, 'Statement')
        Response = apps.get_model(self.django_app_name, 'Response')

        responses = Response.objects.all()

        return Statement.objects.filter(in_response__in=responses)
