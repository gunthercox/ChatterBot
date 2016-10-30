from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Statement, Response
import json


class DjangoStorageAdapter(StorageAdapter):

    def __init__(self, **kwargs):
        super(DjangoStorageAdapter, self).__init__(**kwargs)

        self.adapter_supports_queries = False

    def count(self):
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        return StatementModel.objects.count()

    def model_to_object(self, statement_model):
        """
        Convert a Django model object into a ChatterBot Statement object.
        """
        statement = Statement(
            statement_model.text,
            extra_data=json.loads(statement_model.extra_data, encoding='utf8')
        )

        for response_object in statement_model.in_response_to.all():
            statement.add_response(Response(
                response_object.response.text,
                occurrence=response_object.occurrence
            ))

        return statement

    def find(self, statement_text):
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        try:
            statement = StatementModel.objects.get(
                text=statement_text
            )
            return self.model_to_object(statement)
        except StatementModel.DoesNotExist as e:
            return None

    def filter(self, **kwargs):
        """
        Returns a list of statements in the database
        that match the parameters specified.
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel

        kwargs_copy = kwargs.copy()

        for kwarg in kwargs_copy:
            value = kwargs[kwarg]
            del kwargs[kwarg]
            kwarg = kwarg.replace('__contains', '__response__text')
            kwargs[kwarg] = value

        if 'in_response_to' in kwargs:
            responses = kwargs['in_response_to']
            del kwargs['in_response_to']

            if responses:
                kwargs['in_response_to__response__text__in'] = []
                for response in responses:
                    kwargs['in_response_to__response__text__in'].append(response.text)
            else:
                kwargs['in_response_to'] = None

        statement_objects = StatementModel.objects.filter(**kwargs)

        results = []

        for statement_object in statement_objects:
            results.append(self.model_to_object(statement_object))

        return results

    def update(self, statement, **kwargs):
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        from chatterbot.ext.django_chatterbot.models import Response as ResponseModel
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            django_statement, created = StatementModel.objects.get_or_create(
                text=statement.text,
                extra_data=json.dumps(statement.extra_data)
            )

            for response in statement.in_response_to:
                response_statement, created = StatementModel.objects.get_or_create(
                    text=response.text
                )
                response_object, created = django_statement.in_response_to.get_or_create(
                    statement=statement,
                    response=response_statement
                )
                response_object.occurrence = response.occurrence
                response_object.save()

            django_statement.save()

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        statement = StatementModel.objects.order_by('?').first()
        return self.model_to_object(statement)

    def remove(self, statement_text):
        """
        Removes the statement that matches the input text.
        Removes any responses from statements if the response text matches the
        input text.
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        from chatterbot.ext.django_chatterbot.models import Response as ResponseModel
        from django.db.models import Q
        statements = StatementModel.objects.filter(text=statement_text)

        responses = ResponseModel.objects.filter(
            Q(statement__text=statement_text) | Q(response__text=statement_text)
        )

        responses.delete()
        statements.delete()

    def drop(self):
        """
        Remove all data from the database.
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        from chatterbot.ext.django_chatterbot.models import Response as ResponseModel        

        StatementModel.objects.all().delete()
        ResponseModel.objects.all().delete()