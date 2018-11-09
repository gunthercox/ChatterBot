from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_chatterbot', '0013_change_conversations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statement',
            name='extra_data',
        ),
    ]
