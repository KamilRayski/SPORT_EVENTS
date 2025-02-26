# events/serializers.py
from rest_framework import serializers
from .models import User, Event, Signup, Favorite

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class EventSerializer(serializers.ModelSerializer):
    creator_username = serializers.CharField(source='creator.username', read_only=True)
    creator_email = serializers.EmailField(source='creator.email', read_only=True)
    signups_count = serializers.IntegerField(source='signups.count', read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "address",
            "date",
            "description",
            "capacity",
            "creator",
            "creator_username",
            "creator_email",
            "signups_count",
        ]

class SignupSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Signup
        fields = [
            "id",
            "event",
            "user",
            "user_username",
            "user_email",
        ]

class FavoriteSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.date', read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'event', 'event_title', 'event_date']
