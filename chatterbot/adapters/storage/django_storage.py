from chatterbot.adapters.storage import StorageAdapter
from chatterbot.conversation import Statement, Response


class DjangoStorageAdapter(StorageAdapter):

    def __init__(self, **kwargs):
        super(DjangoStorageAdapter, self).__init__(**kwargs)

    def count(self):
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        return StatementModel.objects.count()

    def model_to_object(self, statement_model):
        """
        Convert a Django model object into a ChatterBot Statement object.
        """
        statement = Statement(statement_model.text)

        for response_object in statement_model.in_response_to:
            statement.add_response(Response(
                response_object.response.text
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

        statement_objects = StatementModel.objects.filter(**kwargs)

        results = []

        for statement_object in statement_objects:
            results.append(self.model_to_object(statement_object))

        return results

    def update(self, statement):
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        from chatterbot.ext.django_chatterbot.models import Response as ResponseModel
        # Do not alter the database unless writing is enabled
        if not self.read_only:
            django_statement, created = StatementModel.objects.get_or_create(
                text=statement.text
            )

            for response in statement.in_response_to:
                response_statement = StatementModel.objects.get_or_create(
                    text=response.text
                )
                django_statement.in_response_to.get_or_create(
                    statement=statement,
                    response=response_statement
                )

            django_statement.save()

        return statement

    def get_random(self):
        """
        Returns a random statement from the database
        """
        from chatterbot.ext.django_chatterbot.models import Statement as StatementModel
        statement = StatementModel.objects.order_by('?').first()
        return self.model_to_object(statement)

    def drop(self):
        """
        Remove the database.
        """
        pass

