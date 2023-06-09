# Generated by Django 3.2.5 on 2021-08-02 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0004_auto_20210803_0019'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('group', 'question')},
        ),
        migrations.CreateModel(
            name='TrueFalseQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField(default=False)),
                ('question', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.question')),
            ],
        ),
    ]
