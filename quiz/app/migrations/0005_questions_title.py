# Generated by Django 4.1.1 on 2022-10-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_questions_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='title',
            field=models.CharField(default='-', max_length=20),
            preserve_default=False,
        ),
    ]
