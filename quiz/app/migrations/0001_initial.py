# Generated by Django 4.1.1 on 2022-10-10 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('subject', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=50, null=True)),
                ('option1', models.CharField(max_length=10)),
                ('option2', models.CharField(max_length=10)),
                ('option3', models.CharField(blank=True, max_length=10, null=True)),
                ('option4', models.CharField(blank=True, max_length=10, null=True)),
                ('public', models.BooleanField(default=True)),
                ('key', models.IntegerField(blank=True, null=True)),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.subjects')),
            ],
        ),
    ]
