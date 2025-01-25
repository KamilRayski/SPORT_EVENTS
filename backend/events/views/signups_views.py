# events/views/signups_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from events.models import Event, User, Signup

@api_view(["POST"])
def signup_for_event(request, event_id):
    """
    POST /events/<event_id>/signups/
    Body JSON: { "name": "...", "email": "..." }
    """
    event = get_object_or_404(Event, id=event_id)

    name = request.data.get("name")
    email = request.data.get("email")

    if not name or not email:
        return Response(
            {"error": "Brak wymaganych danych (name, email)."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if event.signups.count() >= event.capacity:
        return Response(
            {"error": "Brak wolnych miejsc."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user, created = User.objects.get_or_create(email=email)
    if created:
        user.username = name
        user.save()

    already_signed = Signup.objects.filter(event=event, user=user).exists()
    if already_signed:
        return Response(
            {"error": "Użytkownik jest już zapisany na to wydarzenie."},
            status=status.HTTP_400_BAD_REQUEST
        )

    Signup.objects.create(event=event, user=user)

    return Response({"message": "Zapisano pomyślnie!"}, status=status.HTTP_201_CREATED)
