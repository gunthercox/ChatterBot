from django.db import models


class Statement(models.Model):

    text = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=255
    )


class Response(models.Model):

    statement = models.ForeignKey(
        'Statement',
        related_name='in_response_to'
    )

    response = models.ForeignKey(
        'Statement',
        related_name='+'
    )

    unique_together = (('statement', 'response'),)

    occurrence = models.PositiveIntegerField(default=0)

