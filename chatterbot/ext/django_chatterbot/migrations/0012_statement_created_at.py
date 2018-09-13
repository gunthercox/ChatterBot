# -*- coding: utf-8 -*-
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0011_blank_extra_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='created_at',
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text='The date and time that the statement was created at.'
            ),
        ),
    ]
