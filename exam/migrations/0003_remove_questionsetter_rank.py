# Generated by Django 3.2.5 on 2021-07-31 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_question'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionsetter',
            name='rank',
        ),
    ]
