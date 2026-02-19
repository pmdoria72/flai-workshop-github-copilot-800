from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, timedelta
from .models import UserProfile, Team, Activity, Workout, Leaderboard


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            fitness_level='beginner',
            total_points=100
        )
    
    def test_profile_creation(self):
        """Test that profile is created correctly"""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.fitness_level, 'beginner')
        self.assertEqual(self.profile.total_points, 100)
    
    def test_profile_string_representation(self):
        """Test profile string representation"""
        self.assertEqual(str(self.profile), "testuser's profile")


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        """Set up test data"""
        self.captain = User.objects.create_user(
            username='captain',
            email='captain@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='Test description',
            captain=self.captain,
            total_points=500
        )
    
    def test_team_creation(self):
        """Test that team is created correctly"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.captain.username, 'captain')
        self.assertEqual(self.team.total_points, 500)
    
    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')
    
    def test_team_members(self):
        """Test adding members to team"""
        member = User.objects.create_user(
            username='member1',
            email='member1@example.com',
            password='testpass123'
        )
        self.team.members.add(member)
        self.assertEqual(self.team.members.count(), 1)


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories_burned=300
        )
    
    def test_activity_creation(self):
        """Test that activity is created correctly"""
        self.assertEqual(self.activity.user.username, 'testuser')
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)
    
    def test_calculate_points(self):
        """Test points calculation"""
        points = self.activity.calculate_points()
        self.assertEqual(points, 30)  # running: 10 points per 10 minutes = 30 points for 30 minutes


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""
    
    def setUp(self):
        """Set up test data"""
        self.creator = User.objects.create_user(
            username='creator',
            email='creator@example.com',
            password='testpass123'
        )
        self.workout = Workout.objects.create(
            title='Morning Run',
            description='A gentle morning run',
            difficulty_level='beginner',
            activity_type='running',
            duration=20,
            instructions='Run at a steady pace',
            created_by=self.creator
        )
    
    def test_workout_creation(self):
        """Test that workout is created correctly"""
        self.assertEqual(self.workout.title, 'Morning Run')
        self.assertEqual(self.workout.difficulty_level, 'beginner')
        self.assertEqual(self.workout.duration, 20)
    
    def test_workout_string_representation(self):
        """Test workout string representation"""
        self.assertEqual(str(self.workout), 'Morning Run (beginner)')


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        UserProfile.objects.create(user=self.user, fitness_level='beginner')
    
    def test_create_activity(self):
        """Test creating an activity via API"""
        data = {
            'user_id': self.user.id,
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories_burned': 300,
            'date': datetime.now().date().isoformat()
        }
        response = self.client.post('/api/activities/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        self.assertEqual(Activity.objects.get().activity_type, 'running')
    
    def test_list_activities(self):
        """Test listing activities via API"""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.0
        )
        response = self.client.get('/api/activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        """Set up test data"""
        self.captain = User.objects.create_user(
            username='captain',
            email='captain@example.com',
            password='testpass123'
        )
        self.team = Team.objects.create(
            name='Test Team',
            description='Test description',
            captain=self.captain
        )
    
    def test_list_teams(self):
        """Test listing teams via API"""
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_join_team(self):
        """Test joining a team via API"""
        member = User.objects.create_user(
            username='member',
            email='member@example.com',
            password='testpass123'
        )
        response = self.client.post(
            f'/api/teams/{self.team.id}/join/',
            {'user_id': member.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.team.members.count(), 1)


class APIRootTest(APITestCase):
    """Test cases for API root endpoint"""
    
    def test_api_root(self):
        """Test that API root returns list of endpoints"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('users', response.data)
        self.assertIn('profiles', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('workouts', response.data)
        self.assertIn('leaderboard', response.data)
