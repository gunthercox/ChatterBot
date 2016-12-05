from django.db import models


class StatementManager(models.Manager):

    use_for_related_fields = True

    def __len__(self):
        return self.get_queryset().count()

    def __iter__(self):
        for obj in self.get_queryset():
            yield obj
