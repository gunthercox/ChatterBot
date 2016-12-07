from django.db import models


class StatementManager(models.Manager):
    """
    Custom manager for Statement objects.
    """

    def __len__(self):
        return self.get_queryset().count()

    def __iter__(self):
        for obj in self.get_queryset():
            yield obj


class ResponseManager(models.Manager):
    """
    Custom manager for Response objects.
    """

    def __len__(self):
        return self.get_queryset().count()

    def __iter__(self):
        for obj in self.get_queryset():
            yield obj
