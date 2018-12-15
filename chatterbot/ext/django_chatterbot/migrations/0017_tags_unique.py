from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0016_statement_stemmed_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='statements',
        ),
        migrations.AddField(
            model_name='statement',
            name='tags',
            field=models.ManyToManyField(
                related_name='statements',
                to='django_chatterbot.Tag'
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.SlugField(unique=True),
        ),
    ]
