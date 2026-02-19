from django.contrib import admin
from .models import UserProfile, Team, Activity, Workout, Leaderboard


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    list_display = ['user', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['total_points', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'avatar')
        }),
        ('Fitness Details', {
            'fields': ('fitness_level', 'total_points')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team"""
    list_display = ['name', 'captain', 'total_points', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'captain__username']
    readonly_fields = ['total_points', 'created_at', 'updated_at']
    filter_horizontal = ['members']
    
    def member_count(self, obj):
        """Display the number of members in the team"""
        return obj.members.count()
    member_count.short_description = 'Members'
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description', 'captain')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Statistics', {
            'fields': ('total_points',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity"""
    list_display = ['user', 'activity_type', 'duration', 'distance', 'points_earned', 'date', 'created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user__username', 'activity_type', 'notes']
    readonly_fields = ['points_earned', 'created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('user', 'activity_type', 'date')
        }),
        ('Details', {
            'fields': ('duration', 'distance', 'calories_burned', 'notes')
        }),
        ('Points', {
            'fields': ('points_earned',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout"""
    list_display = ['title', 'difficulty_level', 'activity_type', 'duration', 'created_by', 'created_at']
    list_filter = ['difficulty_level', 'activity_type', 'created_at']
    search_fields = ['title', 'description', 'activity_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('title', 'description', 'difficulty_level', 'activity_type')
        }),
        ('Details', {
            'fields': ('duration', 'instructions')
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard"""
    list_display = ['user', 'period', 'rank', 'points', 'period_start', 'period_end', 'updated_at']
    list_filter = ['period', 'period_start', 'period_end']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    date_hierarchy = 'period_start'
    
    fieldsets = (
        ('Leaderboard Entry', {
            'fields': ('user', 'period', 'rank', 'points')
        }),
        ('Period', {
            'fields': ('period_start', 'period_end')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
