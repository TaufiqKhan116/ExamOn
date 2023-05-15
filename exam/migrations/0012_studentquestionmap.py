# Generated by Django 3.2.5 on 2021-12-11 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0011_groupattr_passcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentQuestionMap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.question')),
                ('student', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.student')),
            ],
            options={
                'unique_together': {('question', 'student')},
            },
        ),
    ]
