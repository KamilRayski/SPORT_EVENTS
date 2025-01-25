# events/views/dashboard_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from events.models import User, Event
from django.shortcuts import get_object_or_404

@api_view(["POST"])
def dashboard_events(request):
    """
    POST /dashboard_events/
    Body JSON: { "email": "..." }

    Zwraca listę eventów stworzonych przez usera o wskazanym emailu,
    wraz z listą zapisanych uczestników (username, email).
    """
    email = request.data.get("email")
    if not email:
        return Response(
            {"error": "Brak email w żądaniu."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.filter(email=email).first()
    if not user:
        return Response(
            {"error": "Nie znaleziono użytkownika o podanym emailu."},
            status=status.HTTP_404_NOT_FOUND
        )

    events = Event.objects.filter(creator=user).order_by("-date")

    data = []
    for ev in events:
        signups = ev.signups.select_related("user").all()
        signups_list = []
        for s in signups:
            signups_list.append({
                "username": s.user.username,
                "email": s.user.email
            })
        data.append({
            "event_id": ev.id,
            "title": ev.title,
            "address": ev.address,
            "date": ev.date,
            "capacity": ev.capacity,
            "description": ev.description,
            "signups": signups_list
        })

    return Response(data, status=status.HTTP_200_OK)
