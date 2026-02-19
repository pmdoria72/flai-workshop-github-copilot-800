"""
Django management command to populate the octofit_db database with test data.
Populate the octofit_db database with test data for users, profiles, teams, activities, workouts, and leaderboard.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random

from octofit_tracker.models import UserProfile, Team, Activity, Workout, Leaderboard


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        """Main function to populate the octofit_db database with test data"""
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS('🏃 Starting OctoFit Tracker Database Population'))
        self.stdout.write("=" * 60)
        
        self.stdout.write("\n📝 Step 1: Creating users and profiles...")
        users = self.create_users()
        
        self.stdout.write("\n👥 Step 2: Creating teams...")
        teams = self.create_teams(users)
        
        self.stdout.write("\n🏋️  Step 3: Creating activities...")
        activities = self.create_activities(users)
        
        self.stdout.write("\n💪 Step 4: Creating workout plans...")
        workouts = self.create_workouts()
        
        self.stdout.write("\n🏆 Step 5: Creating leaderboard entries...")
        entries = self.create_leaderboard_entries(users)
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS('✅ Database Population Completed Successfully!'))
        self.stdout.write("=" * 60)
        self.stdout.write(f"\n📊 Summary:")
        self.stdout.write(f"  • Users: {len(users)}")
        self.stdout.write(f"  • Teams: {len(teams)}")
        self.stdout.write(f"  • Activities: {len(activities)}")
        self.stdout.write(f"  • Workouts: {len(workouts)}")
        self.stdout.write(f"  • Leaderboard entries: {len(entries)}")
        self.stdout.write("\n💡 You can now access the API at http://localhost:8000/api/")
        self.stdout.write("=" * 60)

    def create_users(self):
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
                self.stdout.write(self.style.SUCCESS(f"✓ Created user: {user.username}"))
                
                # Create user profile
                profile = UserProfile.objects.create(
                    user=user,
                    bio=f"I'm {user.first_name} and I love fitness!",
                    fitness_level=user_data['fitness_level'],
                    total_points=0
                )
                self.stdout.write(f"  ✓ Created profile for {user.username}")
            else:
                self.stdout.write(f"→ User already exists: {user.username}")
                # Ensure profile exists
                if not hasattr(user, 'profile'):
                    UserProfile.objects.create(
                        user=user,
                        bio=f"I'm {user.first_name} and I love fitness!",
                        fitness_level=user_data['fitness_level'],
                        total_points=0
                    )
                    self.stdout.write(f"  ✓ Created missing profile for {user.username}")
            
            users.append(user)
        
        return users

    def create_teams(self, users):
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
                self.stdout.write(self.style.SUCCESS(f"✓ Created team: {team.name} with {len(team_members)} members"))
            else:
                self.stdout.write(f"→ Team already exists: {team.name}")
            teams.append(team)
        
        return teams

    def create_activities(self, users):
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
            
            self.stdout.write(self.style.SUCCESS(f"✓ Created {num_activities} activities for {user.username}"))
        
        return activities

    def create_workouts(self):
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
                self.stdout.write(self.style.SUCCESS(f"✓ Created workout: {workout.title}"))
            else:
                self.stdout.write(f"→ Workout already exists: {workout.title}")
            workouts.append(workout)
        
        return workouts

    def create_leaderboard_entries(self, users):
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
                self.stdout.write(self.style.SUCCESS(f"✓ Created leaderboard entry for {user.username} (Rank #{rank})"))
            else:
                # Update existing entry
                entry.rank = rank
                entry.points = user.profile.total_points
                entry.save()
                self.stdout.write(f"→ Updated leaderboard entry for {user.username}")
            
            entries.append(entry)
        
        return entries
