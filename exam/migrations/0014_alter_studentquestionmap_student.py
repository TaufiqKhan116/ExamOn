# Generated by Django 3.2.5 on 2021-12-11 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0013_auto_20211212_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentquestionmap',
            name='student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]