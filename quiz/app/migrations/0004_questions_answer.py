# Generated by Django 4.1.1 on 2022-10-22 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_questions_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='answer',
            field=models.CharField(default=1, max_length=1),
            preserve_default=False,
        ),
    ]
