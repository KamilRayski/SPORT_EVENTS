import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from events.models import Event, Signup, User

@csrf_exempt
def signup_for_event(request, event_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return HttpResponseNotFound("Event not found")

        user_name = data.get("name")
        user_email = data.get("email")
        if not user_name or not user_email:
            return JsonResponse({"error": "Brak wymaganych danych (imię, email)."}, status=400)

        signups_count = event.signups.count()
        if signups_count >= event.capacity:
            return JsonResponse({"error": "Brak wolnych miejsc w tym wydarzeniu."}, status=400)

        user, created = User.objects.get_or_create(email=user_email, defaults={'username': user_name})

        existing_signup = Signup.objects.filter(event=event, user=user).first()
        if existing_signup:
            return JsonResponse({"error": "Już jesteś zapisany na to wydarzenie."}, status=400)

        Signup.objects.create(event=event, user=user)
        return JsonResponse({"message": "Zapisano pomyślnie!"}, status=201)

    else:
        return HttpResponseNotAllowed(['POST'])
