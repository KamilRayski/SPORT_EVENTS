# events/views/events_views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.utils import timezone

from events.models import Event, User
from events.serializers import EventSerializer

@api_view(["GET", "POST"])
def events_list_create(request):
    """
    GET  /events/        -> Zwraca listę wszystkich wydarzeń
    POST /events/        -> Tworzy nowe wydarzenie
    """
    if request.method == "GET":
        events = Event.objects.all().order_by("-date")
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        
        title = request.data.get("title")
        address = request.data.get("address")
        date = request.data.get("date")  # format ISO
        capacity = request.data.get("capacity", 10)
        creator_name = request.data.get("creator_name")
        creator_email = request.data.get("creator_email")
        description = request.data.get("description", "")

        if not all([title, creator_name, creator_email, date]):
            return Response(
                {"error": "Brakuje wymaganych pól."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        creator, created = User.objects.get_or_create(email=creator_email)
        if created:
            creator.username = creator_name
            creator.save()

        event = Event.objects.create(
            title=title,
            address=address,
            date=date,
            capacity=capacity,
            description=description,
            creator=creator
        )

        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def event_detail_update_delete(request, event_id):
    """
    GET    /events/<event_id>/      -> Zwraca szczegóły wydarzenia
    PUT    /events/<event_id>/      -> Nadpisuje wydarzenie (wszystkie pola)
    PATCH  /events/<event_id>/      -> Aktualizuje wybrane pola wydarzenia
    DELETE /events/<event_id>/      -> Usuwa wydarzenie
    """
    event = get_object_or_404(Event, id=event_id)

    if request.method == "GET":
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method in ["PUT", "PATCH"]:
        partial = True if request.method == "PATCH" else False
        serializer = EventSerializer(event, data=request.data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
