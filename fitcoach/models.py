from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()

class Profile(BaseModel):
    class Role(models.TextChoices):
        COACH = 'COACH', 'Coach'
        CLIENT = 'CLIENT', 'Client'

    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, db_index=True)
    phone = models.CharField(max_length=11, help_text="Format: 09XXXXXXXXX")
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"

    def is_coach(self):
        return self.role == self.Role.COACH

    def is_client(self):
        return self.role == self.Role.CLIENT

class ClientDetails(BaseModel):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    profile = models.OneToOneField(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='client_details',
        limit_choices_to={'role': Profile.Role.CLIENT}
    )
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=Gender.choices)
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Height in centimeters"
    )
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        help_text="Weight in kilograms"
    )

    class Meta:
        verbose_name_plural = "Client Details"

    def __str__(self):
        return f"Details for {self.profile}"

class ClientGoal(BaseModel):
    class Goal(models.TextChoices):
        LOSE_WEIGHT = 'LOSE_WEIGHT', 'Lose Weight'
        GAIN_WEIGHT = 'GAIN_WEIGHT', 'Gain Weight'
        GAIN_MUSCLE = 'GAIN_MUSCLE', 'Gain Muscle'
        IMPROVE_HEALTH = 'IMPROVE_HEALTH', 'Improve Health'

    client = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='goals',
        limit_choices_to={'role': Profile.Role.CLIENT}
    )
    goal = models.CharField(max_length=20, choices=Goal.choices)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client} - {self.get_goal_display()}"

class CoachClientRelationship(BaseModel):
    coach = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='coached_clients',
        limit_choices_to={'role': Profile.Role.COACH},
        db_index=True
    )
    client = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='coaches',
        limit_choices_to={'role': Profile.Role.CLIENT},
        db_index=True
    )

    class Meta:
        unique_together = ['coach', 'client']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.coach} coaching {self.client}"

    def clean(self):
        if not self.coach.is_coach():
            raise ValidationError("The coach must have a COACH role")
        if not self.client.is_client():
            raise ValidationError("The client must have a CLIENT role")

class ExerciseCategory(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class MuscleGroup(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Exercise(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(
        ExerciseCategory, 
        on_delete=models.CASCADE,
        related_name='exercises',
        db_index=True
    )
    muscle_group = models.ForeignKey(
        MuscleGroup, 
        on_delete=models.CASCADE,
        related_name='exercises',
        db_index=True
    )
    photo = models.ImageField(
        upload_to='exercises/photos/',
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to='exercises/videos/',
        blank=True,
        null=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class CoachExercise(BaseModel):
    coach = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='coach_exercises',
        limit_choices_to={'role': Profile.Role.COACH}
    )
    exercise = models.ForeignKey(
        Exercise, 
        on_delete=models.CASCADE, 
        related_name='coach_exercises'
    )

    class Meta:
        unique_together = ['coach', 'exercise']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.coach} - {self.exercise}"

    def clean(self):
        if not self.coach.is_coach():
            raise ValidationError("Only coaches can be assigned to exercises")

class TrainingProgram(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    coach = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='created_programs',
        limit_choices_to={'role': Profile.Role.COACH}
    )
    exercises = models.ForeignKey(
        CoachExercise,
        on_delete=models.CASCADE,
        related_name='training_programs'
    )

    def __str__(self):
        return self.name

    def clean(self):
        if not self.coach.is_coach():
            raise ValidationError("Only coaches can create training programs")

class ClientTrainingProgramAssignment(BaseModel):
    client = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        related_name='training_program_assignments',
        limit_choices_to={'role': Profile.Role.CLIENT},
        db_index=True
    )
    training_program = models.ForeignKey(
        TrainingProgram,
        on_delete=models.CASCADE,
        related_name='client_assignments',
        db_index=True
    )
    client_details = models.ForeignKey(
        ClientDetails, 
        on_delete=models.CASCADE, 
        related_name='training_program_assignments'
    )
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)

    class Meta:
        ordering = ['-start_date']
        indexes = [
            models.Index(fields=['start_date', 'end_date'], name='date_range_idx'),
        ]

    def __str__(self):
        return f"{self.client} - {self.training_program} ({self.start_date} to {self.end_date})"

    def clean(self):
        if not self.client.is_client():
            raise ValidationError("Only clients can be assigned to training programs")
        if self.end_date < self.start_date:
            raise ValidationError("End date must be after start date")
        if not CoachClientRelationship.objects.filter(
            coach=self.training_program.coach,
            client=self.client,
            deleted_at__isnull=True
        ).exists():
            raise ValidationError("The program's coach must be assigned to this client")