# Generated by Django 4.1.1 on 2022-10-18 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_system', '0003_delete_questions_delete_subjects'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoginForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('passeword', models.CharField(max_length=20)),
            ],
        ),
    ]
