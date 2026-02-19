#!/usr/bin/env python
"""
Script to populate the OctoFit Tracker database with test data.
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'octofit_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from octofit_tracker.models import UserProfile, Team, Activity, Workout, Leaderboard


def create_users():
    """Create test users with profiles"""
    users_data = [
        {'username': 'octocat', 'email': 'octocat@github.com', 'first_name': 'Octo', 'last_name': 'Cat', 'fitness_level': 'intermediate'},
        {'username': 'mona', 'email': 'mona@github.com', 'first_name': 'Mona', 'last_name': 'Lisa', 'fitness_level': 'advanced'},
        {'username': 'hubot', 'email': 'hubot@github.com', 'first_name': 'Hu', 'last_name': 'Bot', 'fitness_level': 'beginner'},
        {'username': 'codercat', 'email': 'codercat@github.com', 'first_name': 'Coder', 'last_name': 'Cat', 'fitness_level': 'intermediate'},
        {'username': 'webhookdog', 'email': 'webhookdog@github.com', 'first_name': 'Webhook', 'last_name': 'Dog', 'fitness_level': 'beginner'},
    ]
    
    users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            print(f"✓ Created user: {user.username}")
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                bio=f"I'm {user.first_name} and I love fitness!",
                fitness_level=user_data['fitness_level'],
                total_points=0
            )
            print(f"  ✓ Created profile for {user.username}")
        else:
            print(f"→ User already exists: {user.username}")
            # Ensure profile exists
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(
                    user=user,
                    bio=f"I'm {user.first_name} and I love fitness!",
                    fitness_level=user_data['fitness_level'],
                    total_points=0
                )
                print(f"  ✓ Created missing profile for {user.username}")
        
        users.append(user)
    
    return users


def create_teams(users):
    """Create test teams"""
    teams_data = [
        {'name': 'Code Crushers', 'description': 'We crush code and workouts!'},
        {'name': 'Commit Champions', 'description': 'Committed to fitness and clean code'},
        {'name': 'Merge Masters', 'description': 'Merging fitness goals with team spirit'},
    ]
    
    teams = []
    for team_data in teams_data:
        team, created = Team.objects.get_or_create(
            name=team_data['name'],
            defaults={
                'description': team_data['description'],
                'captain': random.choice(users),
                'total_points': 0
            }
        )
        if created:
            # Add random members to the team
            team_members = random.sample(users, k=random.randint(2, len(users)))
            team.members.set(team_members)
            team.save()
            print(f"✓ Created team: {team.name} with {len(team_members)} members")
        else:
            print(f"→ Team already exists: {team.name}")
        teams.append(team)
    
    return teams


def create_activities(users):
    """Create test activities"""
    activity_types = ['running', 'walking', 'cycling', 'swimming', 'strength_training', 'yoga', 'sports']
    activities = []
    
    for user in users:
        # Create 5-10 activities per user over the last 30 days
        num_activities = random.randint(5, 10)
        for i in range(num_activities):
            days_ago = random.randint(0, 30)
            activity_date = (datetime.now() - timedelta(days=days_ago)).date()
            
            activity_type = random.choice(activity_types)
            duration = random.randint(15, 120)  # 15 to 120 minutes
            distance = round(random.uniform(1.0, 20.0), 2) if activity_type in ['running', 'cycling', 'walking'] else None
            calories = duration * random.randint(5, 12)
            
            activity = Activity.objects.create(
                user=user,
                activity_type=activity_type,
                duration=duration,
                distance=distance,
                calories_burned=calories,
                date=activity_date,
                notes=f"Great {activity_type} session!"
            )
            
            # Calculate and save points
            activity.points_earned = activity.calculate_points()
            activity.save()
            
            # Update user profile points
            user.profile.total_points += activity.points_earned
            user.profile.save()
            
            activities.append(activity)
        
        print(f"✓ Created {num_activities} activities for {user.username}")
    
    return activities


def create_workouts():
    """Create sample workout plans"""
    workouts_data = [
        {
            'title': 'Morning Jog',
            'description': 'Start your day with a light jog',
            'difficulty_level': 'beginner',
            'activity_type': 'running',
            'duration': 20,
            'instructions': '1. Warm up for 5 minutes\n2. Jog at a comfortable pace for 15 minutes\n3. Cool down and stretch'
        },
        {
            'title': 'HIIT Cardio Blast',
            'description': 'High-intensity interval training for maximum calorie burn',
            'difficulty_level': 'advanced',
            'activity_type': 'sports',
            'duration': 30,
            'instructions': '1. Warm up for 5 minutes\n2. 20 seconds high intensity, 10 seconds rest (repeat 8 times)\n3. Cool down for 5 minutes'
        },
        {
            'title': 'Yoga Flow',
            'description': 'Gentle yoga session for flexibility and relaxation',
            'difficulty_level': 'beginner',
            'activity_type': 'yoga',
            'duration': 30,
            'instructions': '1. Sun salutations x5\n2. Standing poses\n3. Floor poses\n4. Savasana'
        },
        {
            'title': 'Strength Training',
            'description': 'Full body strength workout',
            'difficulty_level': 'intermediate',
            'activity_type': 'strength_training',
            'duration': 45,
            'instructions': '1. Squats 3x10\n2. Push-ups 3x10\n3. Rows 3x10\n4. Planks 3x30sec'
        },
        {
            'title': 'Long Distance Cycle',
            'description': 'Build endurance with a long bike ride',
            'difficulty_level': 'intermediate',
            'activity_type': 'cycling',
            'duration': 60,
            'instructions': '1. Check your bike\n2. Warm up for 10 minutes\n3. Steady pace for 45 minutes\n4. Cool down for 5 minutes'
        },
    ]
    
    workouts = []
    for workout_data in workouts_data:
        workout, created = Workout.objects.get_or_create(
            title=workout_data['title'],
            defaults=workout_data
        )
        if created:
            print(f"✓ Created workout: {workout.title}")
        else:
            print(f"→ Workout already exists: {workout.title}")
        workouts.append(workout)
    
    return workouts


def create_leaderboard_entries(users):
    """Create leaderboard entries for all users"""
    entries = []
    today = datetime.now().date()
    
    # Weekly leaderboard
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    # Sort users by total points
    users_sorted = sorted(users, key=lambda u: u.profile.total_points, reverse=True)
    
    for rank, user in enumerate(users_sorted, start=1):
        entry, created = Leaderboard.objects.get_or_create(
            user=user,
            period='weekly',
            period_start=week_start,
            period_end=week_end,
            defaults={
                'rank': rank,
                'points': user.profile.total_points
            }
        )
        if created:
            print(f"✓ Created leaderboard entry for {user.username} (Rank #{rank})")
        else:
            # Update existing entry
            entry.rank = rank
            entry.points = user.profile.total_points
            entry.save()
            print(f"→ Updated leaderboard entry for {user.username}")
        
        entries.append(entry)
    
    return entries


def main():
    """Main function to populate database"""
    print("=" * 60)
    print("🏃 Starting OctoFit Tracker Database Population")
    print("=" * 60)
    
    print("\n📝 Step 1: Creating users and profiles...")
    users = create_users()
    
    print("\n👥 Step 2: Creating teams...")
    teams = create_teams(users)
    
    print("\n🏋️  Step 3: Creating activities...")
    activities = create_activities(users)
    
    print("\n💪 Step 4: Creating workout plans...")
    workouts = create_workouts()
    
    print("\n🏆 Step 5: Creating leaderboard entries...")
    entries = create_leaderboard_entries(users)
    
    print("\n" + "=" * 60)
    print("✅ Database Population Completed Successfully!")
    print("=" * 60)
    print(f"\n📊 Summary:")
    print(f"  • Users: {len(users)}")
    print(f"  • Teams: {len(teams)}")
    print(f"  • Activities: {len(activities)}")
    print(f"  • Workouts: {len(workouts)}")
    print(f"  • Leaderboard entries: {len(entries)}")
    print("\n💡 You can now access the API at http://localhost:8000/api/")
    print("=" * 60)


if __name__ == '__main__':
    main()
