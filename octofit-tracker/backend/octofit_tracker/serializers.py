from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Team, Activity, Workout, Leaderboard


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['_id', 'user', 'bio', 'avatar', 'fitness_level', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'total_points', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    captain = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'captain', 'members', 'member_count', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'total_points', 'created_at', 'updated_at']

    def get_member_count(self, obj):
        """Return the number of team members"""
        return obj.members.count()

    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Activity
        fields = ['_id', 'user', 'user_id', 'activity_type', 'duration', 'distance', 
                  'calories_burned', 'points_earned', 'notes', 'date', 'created_at']
        read_only_fields = ['_id', 'points_earned', 'created_at']

    def create(self, validated_data):
        """Create activity and calculate points"""
        activity = Activity.objects.create(**validated_data)
        activity.points_earned = activity.calculate_points()
        activity.save()
        
        # Update user's total points
        user_profile = activity.user.profile
        user_profile.total_points += activity.points_earned
        user_profile.save()
        
        return activity

    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    created_by = UserSerializer(read_only=True)
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Workout
        fields = ['_id', 'title', 'description', 'difficulty_level', 'activity_type', 
                  'duration', 'instructions', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    user = UserSerializer(read_only=True)
    _id = serializers.CharField(read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user', 'period', 'rank', 'points', 'period_start', 'period_end', 'updated_at']
        read_only_fields = ['_id', 'updated_at']

    def to_representation(self, instance):
        """Convert ObjectId to string"""
        representation = super().to_representation(instance)
        if representation.get('_id'):
            representation['_id'] = str(representation['_id'])
        return representation
