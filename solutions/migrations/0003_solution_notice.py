# Generated by Django 4.0.1 on 2022-03-21 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0002_solution_solution_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='notice',
            field=models.TextField(blank=True, null=True),
        ),
    ]
