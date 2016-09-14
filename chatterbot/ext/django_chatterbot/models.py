from django.db import models


class Statement(models.Model):

    text = models.CharField(
        unique=True,
        blank=False,
        null=False,
        max_length=255
    )

    def __str__(self):
        return '{}...'.format(self.text[:57]) if len(self.text) > 60 else self.text


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

    def __str__(self):
        s = self.statement.text if len(self.statement.text) <= 20 else self.statement.text[:17] + '...'
        s += '\n => '
        s += self.response.text if len(self.response.text) <= 40 else self.statement.text[:37] + '...'
        return s
