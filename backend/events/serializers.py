from rest_framework import serializers
from .models import User, Event, Signup

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class EventSerializer(serializers.ModelSerializer):
    # Pola tylko do odczytu, wyprowadzone z powiązanego obiektu `creator`
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
