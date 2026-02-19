from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import UserProfile, Team, Activity, Workout, Leaderboard
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    TeamSerializer, 
    ActivitySerializer, 
    WorkoutSerializer, 
    LeaderboardSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user statistics"""
        user = self.get_object()
        activities = Activity.objects.filter(user=user)
        
        stats = {
            'total_activities': activities.count(),
            'total_points': activities.aggregate(Sum('points_earned'))['points_earned__sum'] or 0,
            'total_duration': activities.aggregate(Sum('duration'))['duration__sum'] or 0,
            'total_distance': activities.aggregate(Sum('distance'))['distance__sum'] or 0,
        }
        return Response(stats)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile model"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top performing users by points"""
        top_profiles = UserProfile.objects.order_by('-total_points')[:10]
        serializer = self.get_serializer(top_profiles, many=True)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """ViewSet for Team model"""
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Join a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            team.members.add(user)
            return Response({'status': 'joined', 'team': team.name})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Leave a team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        try:
            user = User.objects.get(id=user_id)
            team.members.remove(user)
            return Response({'status': 'left', 'team': team.name})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def leaderboard(self, request, pk=None):
        """Get team leaderboard"""
        team = self.get_object()
        members = team.members.all()
        
        member_stats = []
        for member in members:
            profile = member.profile
            member_stats.append({
                'user': UserSerializer(member).data,
                'total_points': profile.total_points,
            })
        
        # Sort by total_points descending
        member_stats.sort(key=lambda x: x['total_points'], reverse=True)
        return Response(member_stats)


class ActivityViewSet(viewsets.ModelViewSet):
    """ViewSet for Activity model"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        """Filter activities by user if specified"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        activity_type = self.request.query_params.get('activity_type', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        return queryset

    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent activities across all users"""
        recent_activities = Activity.objects.all()[:20]
        serializer = self.get_serializer(recent_activities, many=True)
        return Response(serializer.data)


class WorkoutViewSet(viewsets.ModelViewSet):
    """ViewSet for Workout model"""
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    def get_queryset(self):
        """Filter workouts by difficulty level if specified"""
        queryset = Workout.objects.all()
        difficulty = self.request.query_params.get('difficulty', None)
        activity_type = self.request.query_params.get('activity_type', None)
        
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
            
        return queryset

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended workouts based on user's fitness level"""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(id=user_id)
            user_profile = user.profile
            workouts = Workout.objects.filter(difficulty_level=user_profile.fitness_level)[:5]
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """ViewSet for Leaderboard model"""
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        """Filter leaderboard by period if specified"""
        queryset = Leaderboard.objects.all()
        period = self.request.query_params.get('period', None)
        
        if period:
            queryset = queryset.filter(period=period)
            
        return queryset

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current period leaderboard"""
        period = request.query_params.get('period', 'weekly')
        
        # Calculate current period dates
        today = datetime.now().date()
        if period == 'daily':
            period_start = today
            period_end = today
        elif period == 'weekly':
            period_start = today - timedelta(days=today.weekday())
            period_end = period_start + timedelta(days=6)
        elif period == 'monthly':
            period_start = today.replace(day=1)
            next_month = today.replace(day=28) + timedelta(days=4)
            period_end = next_month - timedelta(days=next_month.day)
        else:  # all_time
            period_start = datetime(2000, 1, 1).date()
            period_end = today
        
        leaderboard = Leaderboard.objects.filter(
            period=period,
            period_start=period_start,
            period_end=period_end
        ).order_by('rank')[:10]
        
        serializer = self.get_serializer(leaderboard, many=True)
        return Response(serializer.data)
