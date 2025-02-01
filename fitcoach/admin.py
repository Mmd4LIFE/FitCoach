from django.contrib import admin
from .models import (
    Profile, ClientDetails, ClientGoal, CoachClientRelationship,
    ExerciseCategory, MuscleGroup, Exercise, CoachExercise,
    TrainingProgram, ClientTrainingProgramAssignment
)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')
    date_hierarchy = 'created_at'

@admin.register(ClientDetails)
class ClientDetailsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'gender', 'birth_date', 'height', 'weight')
    list_filter = ('gender',)
    search_fields = ('profile__user__username',)

@admin.register(ClientGoal)
class ClientGoalAdmin(admin.ModelAdmin):
    list_display = ('client', 'goal', 'created_at')
    list_filter = ('goal', 'created_at')
    search_fields = ('client__user__username',)

@admin.register(CoachClientRelationship)
class CoachClientRelationshipAdmin(admin.ModelAdmin):
    list_display = ('coach', 'client', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('coach__user__username', 'client__user__username')
    date_hierarchy = 'created_at'

@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'muscle_group', 'created_at')
    list_filter = ('category', 'muscle_group')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'

@admin.register(CoachExercise)
class CoachExerciseAdmin(admin.ModelAdmin):
    list_display = ('coach', 'exercise', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('coach__user__username', 'exercise__name')

@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'coach', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description', 'coach__user__username')
    date_hierarchy = 'created_at'

@admin.register(ClientTrainingProgramAssignment)
class ClientTrainingProgramAssignmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'training_program', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('client__user__username', 'training_program__name')
    date_hierarchy = 'start_date'
