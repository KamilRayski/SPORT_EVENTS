# events/views/auth_views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from events.models import User
from rest_framework_simplejwt.views import TokenObtainPairView

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    POST /auth/register/
    Body JSON: { "username": "...", "email": "...", "password": "..." }
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    if not all([username, email, password]):
        return Response({"error": "Wszystkie pola są wymagane."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Użytkownik z tym adresem email już istnieje."}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, email=email)
    user.set_password(password)
    user.save()

    return Response({"message": "Rejestracja przebiegła pomyślnie."}, status=status.HTTP_201_CREATED)

# Dodajemy login_view jako alias dla gotowego widoku
login_view = TokenObtainPairView.as_view()
