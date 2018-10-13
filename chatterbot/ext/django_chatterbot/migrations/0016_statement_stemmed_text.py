from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0015_statement_persona'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='stemmed_text',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
