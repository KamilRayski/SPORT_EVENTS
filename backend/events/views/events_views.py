import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from events.models import Event, User
from django.db.models import F

@csrf_exempt
def events_list_create(request):
    if request.method == 'GET':
        all_events = Event.objects.all()
        result = []
        for ev in all_events:
            result.append({
                "id": ev.id,
                "title": ev.title,
                "address": ev.address,
                "date": ev.date.isoformat(),
                "capacity": ev.capacity,
                "description": ev.description,
                "creator_username": ev.creator.username if ev.creator else None,
                "creator_email": ev.creator.email if ev.creator else None
            })
        return JsonResponse(result, safe=False, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        raw_date = data.get("date")
        parsed_date = parse_datetime(raw_date) if raw_date else None

        creator_name = data.get("creator_name")
        creator_email = data.get("creator_email")
        if not creator_name or not creator_email:
            return JsonResponse({"error": "Musisz podać zarówno nazwę organizatora, jak i e-mail."}, status=400)

        user, created = User.objects.get_or_create(email=creator_email, defaults={
            'username': creator_name,
        })

        new_event = Event.objects.create(
            title=data.get("title"),
            address=data.get("address"),
            date=parsed_date or None,
            capacity=data.get("capacity", 10),
            description=data.get("description"),
            creator=user
        )

        return JsonResponse({"message": "Event created", "id": new_event.id}, status=201)

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])
    

@csrf_exempt
def event_detail_update_delete(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return HttpResponseNotFound("Event not found")

    if request.method == 'GET':
        signups_count = event.signups.count()
        free_spots = event.capacity - signups_count
        data = {
            "id": event.id,
            "title": event.title,
            "address": event.address,
            "date": event.date.isoformat(),
            "description": event.description,
            "capacity": event.capacity,
            "creator_username": event.creator.username if event.creator else None,
            "creator_email": event.creator.email if event.creator else None,
            "signups_count": signups_count,
            "free_spots": free_spots
        }
        return JsonResponse(data, status=200)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        creator_email = data.get("creator_email")
        if not creator_email:
            return JsonResponse({"error": "Nie podano emaila organizatora."}, status=400)

        if event.creator.email != creator_email:
            return JsonResponse({"error": "Only the creator can perform this action!"}, status=403)

        event.title = data.get("title", event.title)
        event.address = data.get("address", event.address)

        if data.get("date"):
            parsed_date = parse_datetime(data["date"])
            if parsed_date:
                event.date = parsed_date

        if data.get("capacity") is not None:
            event.capacity = data["capacity"]

        if data.get("description") is not None:
            event.description = data["description"]

        event.save()
        return JsonResponse({"message": "Event updated"}, status=200)

    elif request.method == 'DELETE':
        # Sprawdzamy email organizatora
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        creator_email = data.get("creator_email")
        if not creator_email:
            return JsonResponse({"error": "Nie podano emaila organizatora."}, status=400)

        if event.creator.email != creator_email:
            return JsonResponse({"error": "Only the creator can perform this action!"}, status=403)

        event.delete()
        return JsonResponse({"message": "Event deleted"}, status=200)

    else:
        return HttpResponseNotAllowed(['GET', 'PUT', 'DELETE'])
