# Generated by Django 3.2.5 on 2021-07-31 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=200)),
                ('question', models.CharField(max_length=500)),
                ('setter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.questionsetter')),
            ],
        ),
    ]