# Generated by Django 3.2 on 2021-12-13 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0020_groupattr_published'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groupattr',
            old_name='published',
            new_name='isPublished',
        ),
    ]