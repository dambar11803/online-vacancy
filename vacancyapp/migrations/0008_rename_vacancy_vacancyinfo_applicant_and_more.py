# Generated by Django 5.1.6 on 2025-02-27 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancyapp', '0007_remove_applicantinfo_applied_to_vacancyinfo_vacancy'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vacancyinfo',
            old_name='vacancy',
            new_name='applicant',
        ),
        migrations.AlterField(
            model_name='vacancyinfo',
            name='vacancy_level',
            field=models.IntegerField(choices=[(4, 4), (5, 5), (6, 6)], default=4),
        ),
        migrations.CreateModel(
            name='EducationInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('Plus2', 'Plus2'), ('Bachelor', 'Bachelor'), ('Master', 'Master')], default='Plus2', max_length=50)),
                ('faculty', models.CharField(choices=[('IT', 'IT'), ('Commerce', 'Commerce')], default='Commerce', max_length=50)),
                ('course_name', models.CharField(max_length=50)),
                ('university_name', models.CharField(choices=[('Pokhara University', 'Pokhara University'), ('Purbanchal University', 'Purbanchal University'), ('Tribhuwan University', 'Tribhuwan University')], default='Tribhuwan University', max_length=100)),
                ('college_name', models.CharField(max_length=100)),
                ('passed_year', models.CharField(max_length=4)),
                ('grade_percent', models.CharField(max_length=4)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vacancyapp.applicantinfo')),
            ],
        ),
    ]
