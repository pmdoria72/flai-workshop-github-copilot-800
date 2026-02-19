from djongo import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for OctoFit Tracker"""
    _id = models.ObjectIdField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'userprofiles'

    def __str__(self):
        return f"{self.user.username}'s profile"


class Team(models.Model):
    """Team model for group competitions"""
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    captain = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='teams_captained')
    members = models.ManyToManyField(User, related_name='teams', blank=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity logging model"""
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(
        max_length=50,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('sports', 'Sports'),
            ('other', 'Other')
        ]
    )
    duration = models.IntegerField(help_text="Duration in minutes")
    distance = models.FloatField(null=True, blank=True, help_text="Distance in kilometers")
    calories_burned = models.IntegerField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} on {self.date}"

    def calculate_points(self):
        """Calculate points based on activity type and duration"""
        base_points = {
            'running': 10,
            'walking': 5,
            'cycling': 8,
            'swimming': 12,
            'strength_training': 8,
            'yoga': 6,
            'sports': 9,
            'other': 5
        }
        points_per_minute = base_points.get(self.activity_type, 5)
        return points_per_minute * (self.duration // 10)


class Workout(models.Model):
    """Personalized workout suggestions"""
    _id = models.ObjectIdField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ]
    )
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField(help_text="Estimated duration in minutes")
    instructions = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_workouts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['difficulty_level', 'title']

    def __str__(self):
        return f"{self.title} ({self.difficulty_level})"


class Leaderboard(models.Model):
    """Leaderboard entry for tracking rankings"""
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    period = models.CharField(
        max_length=20,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('all_time', 'All Time')
        ]
    )
    rank = models.IntegerField()
    points = models.IntegerField()
    period_start = models.DateField()
    period_end = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['period', 'rank']
        unique_together = ['user', 'period', 'period_start']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.period})"
