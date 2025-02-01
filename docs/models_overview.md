# FitCoach Models Documentation

## Core Models

### Profile
- Represents both coaches and clients in the system
- Extends from User model
- Has two roles: COACH and CLIENT
- Contains basic info: phone and bio
- Methods to check role: `is_coach()` and `is_client()`

### ClientDetails
- Extended information for clients only
- Contains: birth date, gender, height, weight
- One-to-one relationship with Profile (Client role only)

### ClientGoal
- Tracks fitness goals for clients
- Goals include: Lose Weight, Gain Weight, Gain Muscle, Improve Health
- Multiple goals can be set per client

### CoachClientRelationship
- Maps the relationship between coaches and their clients
- Ensures proper role validation
- Unique pairing between coach and client

## Exercise Related Models

### ExerciseCategory
- Categorizes different types of exercises
- Contains name and description

### MuscleGroup
- Defines different muscle groups
- Contains name and description

### Exercise
- Core exercise information
- Includes name, description, category, and muscle group
- Supports photo and video attachments
- Linked to both ExerciseCategory and MuscleGroup

### CoachExercise
- Links coaches to their exercises
- Allows coaches to maintain their exercise library
- Unique pairing between coach and exercise

## Training Program Models

### TrainingProgram
- Represents a complete training program
- Created by coaches
- Contains name, description
- Links to exercises through CoachExercise

### ClientTrainingProgramAssignment
- Assigns training programs to clients
- Includes start and end dates
- Links to client details
- Validates coach-client relationship

## Common Features

All models inherit from BaseModel which provides:
- Created at timestamp
- Updated at timestamp
- Soft delete capability
- Automatic timestamp management

## Key Relationships

1. Coach -> Client (through CoachClientRelationship)
2. Client -> ClientDetails (one-to-one)
3. Coach -> Exercises (through CoachExercise)
4. Training Program -> Exercises
5. Client -> Training Programs (through ClientTrainingProgramAssignment)

## Usage Guidelines

1. Always check role validations when working with Profile model
2. Use soft delete when removing records (`soft_delete()` method)
3. Ensure proper date validations for program assignments
4. Verify coach-client relationships before program assignments
5. Use the provided indexes for optimal query performance

## Database Indexes

Key indexes are implemented on:
- Profile creation date
- Exercise name
- Training program name
- Assignment date ranges
- Coach-client relationships

## Model Validation

Most models include validation through the `clean()` method:
- Role validation for coaches and clients
- Date range validation for program assignments
- Relationship validation for coach-client assignments

This structure provides a robust foundation for building a fitness coaching application with clear separation of concerns and proper relationship management. 