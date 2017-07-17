# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('occurrence', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Statement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='response',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='django_chatterbot.Statement'),
        ),
        migrations.AddField(
            model_name='response',
            name='statement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='in_response_to', to='django_chatterbot.Statement'),
        ),
    ]
