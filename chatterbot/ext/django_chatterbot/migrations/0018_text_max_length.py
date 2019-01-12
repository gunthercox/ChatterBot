from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0017_tags_unique'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statement',
            name='in_response_to',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='statement',
            name='search_in_response_to',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='statement',
            name='search_text',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='statement',
            name='text',
            field=models.CharField(max_length=255),
        ),
    ]
