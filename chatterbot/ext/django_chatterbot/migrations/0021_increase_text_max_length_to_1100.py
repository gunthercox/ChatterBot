"""
Django migration to increase text field max_length from 255 to 1100.

This migration alters all text-related fields in the Statement model:
- text
- search_text
- in_response_to
- search_in_response_to

This change supports longer conversational statements while remaining
within VARCHAR limits for most databases.
"""
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0020_alter_statement_conversation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='text',
            field=models.CharField(max_length=1100, help_text='The text of the statement.'),
        ),
        migrations.AlterField(
            model_name='statement',
            name='search_text',
            field=models.CharField(
                blank=True,
                max_length=1100,
                help_text='A modified version of the statement text optimized for searching.'
            ),
        ),
        migrations.AlterField(
            model_name='statement',
            name='in_response_to',
            field=models.CharField(
                max_length=1100,
                null=True,
                help_text='The text of the statement that this statement is in response to.'
            ),
        ),
        migrations.AlterField(
            model_name='statement',
            name='search_in_response_to',
            field=models.CharField(
                blank=True,
                max_length=1100,
                help_text='A modified version of the in_response_to text optimized for searching.'
            ),
        ),
    ]
