# events/views/favorites_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from events.models import Favorite, Event
from events.serializers import FavoriteSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    serializer = FavoriteSerializer(favorites, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite(request):
    user = request.user
    event_id = request.data.get("event_id")
    if not event_id:
        return Response({"error": "Brak event_id."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
    if Favorite.objects.filter(user=user, event=event).exists():
        return Response({"error": "Event już dodany do ulubionych."}, status=status.HTTP_400_BAD_REQUEST)
    favorite = Favorite.objects.create(user=user, event=event)
    serializer = FavoriteSerializer(favorite)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, favorite_id):
    user = request.user
    try:
        favorite = Favorite.objects.get(id=favorite_id, user=user)
    except Favorite.DoesNotExist:
        return Response({"error": "Ulubiony event nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
    favorite.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
