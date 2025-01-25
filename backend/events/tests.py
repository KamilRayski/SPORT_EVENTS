# events/tests.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import User, Event, Signup


class EventViewsTestCase(APITestCase):
    def setUp(self):
        """
        Przygotowanie danych testowych:
         - dwóch użytkowników
         - dwa wydarzenia (jedno przypisane do user_a, drugie do user_b)
        """
        self.user_a = User.objects.create(username="John", email="john@example.com")
        self.user_b = User.objects.create(username="Alice", email="alice@example.com")

        self.event_a = Event.objects.create(
            title="Event A",
            address="Kraków, Rynek Główny 1",
            capacity=10,
            creator=self.user_a
        )
        self.event_b = Event.objects.create(
            title="Event B",
            address="Warszawa, ul. Marszałkowska 10",
            capacity=5,
            creator=self.user_b
        )

        # URL-e zdefiniowane w urls.py (name=...)
        self.events_list_create_url = reverse("events-list-create")
        # Uwaga: event-detail wymaga argumentu, np. reverse('event-detail', kwargs={'event_id': 123})
        # będziemy go generować dynamicznie w testach

    def test_events_list(self):
        """Sprawdza, czy endpoint /events/ (GET) zwraca listę 2 wydarzeń."""
        response = self.client.get(self.events_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)
        # Sprawdzamy, czy tytuły się zgadzają
        titles = {event["title"] for event in data}
        self.assertIn("Event A", titles)
        self.assertIn("Event B", titles)

    def test_create_event_success(self):
        """Sprawdza, czy możemy utworzyć nowe wydarzenie za pomocą /events/ (POST)."""
        payload = {
            "title": "Nowe Wydarzenie",
            "address": "Łódź, ul. Piotrkowska 15",
            "date": "2025-01-01T12:00:00Z",
            "capacity": 20,
            "creator_name": "Bob",
            "creator_email": "bob@example.com",
            "description": "Opis wydarzenia testowego"
        }
        response = self.client.post(self.events_list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Sprawdzamy, czy wydarzenie pojawiło się w bazie
        created_event = Event.objects.filter(title="Nowe Wydarzenie").first()
        self.assertIsNotNone(created_event)
        self.assertEqual(created_event.address, "Łódź, ul. Piotrkowska 15")
        self.assertEqual(created_event.capacity, 20)

        # Sprawdzamy, czy user (creator) został utworzony/odnaleziony
        self.assertEqual(created_event.creator.email, "bob@example.com")
        self.assertEqual(created_event.creator.username, "Bob")

    def test_create_event_missing_fields(self):
        """Sprawdza próbę utworzenia wydarzenia bez wymaganych pól (title, creator_name, creator_email, date)."""
        payload = {
            "address": "Brak daty i tytułu",
        }
        response = self.client.post(self.events_list_create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_data = response.json()
        self.assertIn("error", error_data)

    def test_event_detail_get(self):
        """Sprawdza GET /events/<id>/ dla istniejącego wydarzenia."""
        url = reverse("event-detail", kwargs={"event_id": self.event_a.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(data["id"], self.event_a.id)
        self.assertEqual(data["title"], "Event A")
        self.assertEqual(data["creator_username"], self.user_a.username)

    def test_event_detail_put(self):
        """Sprawdza PUT /events/<id>/"""
        url = reverse("event-detail", kwargs={"event_id": self.event_a.id})
        payload = {
            "title": "Event A - updated",
            "address": "Nowy adres",
            "date": "2025-05-05T10:00:00Z",
            "capacity": 100,
            "creator": self.user_a.id,  # trzeba przesłać id usera przy PUT
            "description": "Zmieniony opis"
        }
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.event_a.refresh_from_db()
        self.assertEqual(self.event_a.title, "Event A - updated")
        self.assertEqual(self.event_a.address, "Nowy adres")
        self.assertEqual(self.event_a.capacity, 100)
        self.assertEqual(self.event_a.description, "Zmieniony opis")

    def test_event_detail_delete(self):
        """Sprawdza DELETE /events/<id>/"""
        url = reverse("event-detail", kwargs={"event_id": self.event_b.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Sprawdzamy, czy event został usunięty
        exists = Event.objects.filter(id=self.event_b.id).exists()
        self.assertFalse(exists)


class SignupsViewsTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="Tester", email="tester@example.com")
        self.event = Event.objects.create(
            title="Test Event",
            address="Gdańsk",
            capacity=2,
            creator=self.user
        )
        self.signup_url = reverse("event-signup", kwargs={"event_id": self.event.id})

    def test_signup_for_event_success(self):
        """Sprawdza poprawny zapis na wydarzenie."""
        payload = {
            "name": "Nowy Użytkownik",
            "email": "newuser@example.com"
        }
        response = self.client.post(self.signup_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Sprawdzamy, czy signup został zapisany
        signup_exists = Signup.objects.filter(
            event=self.event,
            user__email="newuser@example.com"
        ).exists()
        self.assertTrue(signup_exists)

    def test_signup_for_event_already_signed(self):
        """Sprawdza zapis na wydarzenie dla usera, który już istnieje w signups."""
        # Najpierw zapisujemy jednego usera
        Signup.objects.create(event=self.event, user=self.user)  # self.user.email = tester@example.com

        payload = {
            "name": "Tester updated name",  # username może się zmienić, ale email jest kluczem
            "email": "tester@example.com"
        }
        response = self.client.post(self.signup_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_data = response.json()
        self.assertIn("error", error_data)
        self.assertIn("Użytkownik jest już zapisany", error_data["error"])

    def test_signup_for_event_no_capacity(self):
        """Sprawdza zapis na wydarzenie, gdy brakuje miejsc."""
        # capacity = 2, zapełniamy 2 miejsca
        user2 = User.objects.create(username="User2", email="user2@example.com")
        Signup.objects.create(event=self.event, user=self.user)   # 1. tester@example.com
        Signup.objects.create(event=self.event, user=user2)       # 2. user2@example.com

        # Próbujemy zapisać kolejnego
        payload = {
            "name": "OverflowUser",
            "email": "overflow@example.com"
        }
        response = self.client.post(self.signup_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_data = response.json()
        self.assertIn("error", error_data)
        self.assertIn("Brak wolnych miejsc", error_data["error"])


class DashboardViewsTestCase(APITestCase):
    def setUp(self):
        # Tworzymy użytkownika, który ma 2 wydarzenia
        self.user_owner = User.objects.create(username="Owner", email="owner@example.com")
        self.event1 = Event.objects.create(
            title="Owner's Event 1",
            address="Some Address 1",
            creator=self.user_owner
        )
        self.event2 = Event.objects.create(
            title="Owner's Event 2",
            address="Some Address 2",
            creator=self.user_owner
        )
        # Tworzymy innego usera + signup
        self.user_participant = User.objects.create(username="Participant", email="part@example.com")
        Signup.objects.create(event=self.event1, user=self.user_participant)

        self.dashboard_url = reverse("dashboard-events")

    def test_dashboard_correct_email(self):
        """
        Sprawdza, czy zwracane są wydarzenia dla usera o emailu owner@example.com,
        wraz z listą zapisanych uczestników.
        """
        payload = {"email": "owner@example.com"}
        response = self.client.post(self.dashboard_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(len(data), 2)  # 2 wydarzenia
        # W jednym z nich (event1) powinna być 1 osoba zapisana
        event_with_signups = [ev for ev in data if ev["title"] == "Owner's Event 1"][0]
        self.assertEqual(len(event_with_signups["signups"]), 1)
        self.assertEqual(event_with_signups["signups"][0]["email"], "part@example.com")

    def test_dashboard_missing_email(self):
        """
        Sprawdza reakcję na brak emaila w zapytaniu POST.
        """
        response = self.client.post(self.dashboard_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_data = response.json()
        self.assertIn("error", error_data)

    def test_dashboard_not_found_user(self):
        """
        Sprawdza reakcję na sytuację, gdy użytkownik o podanym emailu nie istnieje.
        """
        payload = {"email": "not_existed@example.com"}
        response = self.client.post(self.dashboard_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        error_data = response.json()
        self.assertIn("error", error_data)
        self.assertIn("Nie znaleziono użytkownika", error_data["error"])
