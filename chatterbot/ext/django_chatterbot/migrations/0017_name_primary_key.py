from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0016_statement_stemmed_text'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='id',
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.SlugField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tag',
            name='statements',
            field=models.ManyToManyField(related_name='tags', to='django_chatterbot.Statement'),
        ),
    ]
