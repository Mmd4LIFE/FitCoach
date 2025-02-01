# Generated by Django 5.1.5 on 2025-02-01 17:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], max_length=10)),
                ('height', models.DecimalField(decimal_places=2, help_text='Height in centimeters', max_digits=5)),
                ('weight', models.DecimalField(decimal_places=2, help_text='Weight in kilograms', max_digits=5)),
            ],
            options={
                'verbose_name_plural': 'Client Details',
            },
        ),
        migrations.CreateModel(
            name='ExerciseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MuscleGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='exercises/photos/')),
                ('video', models.FileField(blank=True, null=True, upload_to='exercises/videos/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='fitcoach.exercisecategory')),
                ('muscle_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='fitcoach.musclegroup')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('role', models.CharField(choices=[('COACH', 'Coach'), ('CLIENT', 'Client')], db_index=True, max_length=10)),
                ('phone', models.CharField(help_text='Format: 09XXXXXXXXX', max_length=11)),
                ('bio', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CoachExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coach_exercises', to='fitcoach.exercise')),
                ('coach', models.ForeignKey(limit_choices_to={'role': 'COACH'}, on_delete=django.db.models.deletion.CASCADE, related_name='coach_exercises', to='fitcoach.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='CoachClientRelationship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('client', models.ForeignKey(limit_choices_to={'role': 'CLIENT'}, on_delete=django.db.models.deletion.CASCADE, related_name='coaches', to='fitcoach.profile')),
                ('coach', models.ForeignKey(limit_choices_to={'role': 'COACH'}, on_delete=django.db.models.deletion.CASCADE, related_name='coached_clients', to='fitcoach.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ClientGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('goal', models.CharField(choices=[('LOSE_WEIGHT', 'Lose Weight'), ('GAIN_WEIGHT', 'Gain Weight'), ('GAIN_MUSCLE', 'Gain Muscle'), ('IMPROVE_HEALTH', 'Improve Health')], max_length=20)),
                ('client', models.ForeignKey(limit_choices_to={'role': 'CLIENT'}, on_delete=django.db.models.deletion.CASCADE, related_name='goals', to='fitcoach.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ClientExerciseAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('start_date', models.DateField(db_index=True)),
                ('end_date', models.DateField(db_index=True)),
                ('client_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_assignments', to='fitcoach.clientdetails')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_assignments', to='fitcoach.exercise')),
                ('client', models.ForeignKey(limit_choices_to={'role': 'CLIENT'}, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_assignments', to='fitcoach.profile')),
            ],
            options={
                'ordering': ['-start_date'],
            },
        ),
        migrations.AddField(
            model_name='clientdetails',
            name='profile',
            field=models.OneToOneField(limit_choices_to={'role': 'CLIENT'}, on_delete=django.db.models.deletion.CASCADE, related_name='client_details', to='fitcoach.profile'),
        ),
        migrations.AddIndex(
            model_name='profile',
            index=models.Index(fields=['created_at'], name='fitcoach_pr_created_445732_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='coachexercise',
            unique_together={('coach', 'exercise')},
        ),
        migrations.AddIndex(
            model_name='coachclientrelationship',
            index=models.Index(fields=['created_at'], name='fitcoach_co_created_04afc8_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='coachclientrelationship',
            unique_together={('coach', 'client')},
        ),
        migrations.AddIndex(
            model_name='clientexerciseassignment',
            index=models.Index(fields=['start_date', 'end_date'], name='date_range_idx'),
        ),
    ]
