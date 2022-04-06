# Generated by Django 4.0.1 on 2022-03-24 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('problems', '0002_problem'),
        ('solutions', '0003_solution_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='Distribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('date_result', models.DateTimeField(blank=True, null=True)),
                ('result', models.IntegerField(default=0)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distribution', to='problems.problem')),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distribution', to='solutions.solution')),
            ],
        ),
    ]