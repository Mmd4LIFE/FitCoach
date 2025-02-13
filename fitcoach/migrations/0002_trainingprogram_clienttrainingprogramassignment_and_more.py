# Generated by Django 5.1.5 on 2025-02-01 17:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitcoach', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField()),
                ('coach', models.ForeignKey(limit_choices_to={'role': 'COACH'}, on_delete=django.db.models.deletion.CASCADE, related_name='created_programs', to='fitcoach.profile')),
                ('exercises', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_programs', to='fitcoach.coachexercise')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ClientTrainingProgramAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(db_index=True)),
                ('client', models.ForeignKey(limit_choices_to={'role': 'CLIENT'}, on_delete=django.db.models.deletion.CASCADE, related_name='training_program_assignments', to='fitcoach.profile')),
                ('client_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_program_assignments', to='fitcoach.clientdetails')),
                ('training_program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_assignments', to='fitcoach.trainingprogram')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.DeleteModel(
            name='ClientExerciseAssignment',
        ),
        migrations.AddIndex(
            model_name='clienttrainingprogramassignment',
            index=models.Index(fields=['start_date', 'end_date'], name='date_range_idx'),
        ),
    ]
