import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from events.models import User

@csrf_exempt
def dashboard_events(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest("Invalid JSON")

        email = data.get("email")
        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        events = user.events_created.all()
        response = []
        for ev in events:
            signups_list = []
            for signup in ev.signups.all():
                signups_list.append({
                    "username": signup.user.username,
                    "email": signup.user.email
                })
            response.append({
                "event_id": ev.id,
                "title": ev.title,
                "address": ev.address,
                "date": ev.date.isoformat(),
                "description": ev.description,
                "capacity": ev.capacity,
                "signups": signups_list
            })

        return JsonResponse(response, safe=False, status=200)

    else:
        return HttpResponseNotAllowed(['POST'])
