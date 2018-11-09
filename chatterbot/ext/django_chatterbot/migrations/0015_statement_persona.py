from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0014_remove_statement_extra_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='statement',
            name='persona',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
