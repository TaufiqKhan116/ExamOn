# Generated by Django 3.2.5 on 2021-12-11 16:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0008_groupattr'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionsetter',
            old_name='isVarified',
            new_name='isVerified',
        ),
    ]