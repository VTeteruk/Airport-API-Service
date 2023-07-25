from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from airplanes.models import Airplane, AirplaneType
from crews.models import Crew, Position
from flights.models import Airport, City, Route

FLIGHT_URL = reverse("flights:flight-list")


class UnauthenticatedFlightTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(FLIGHT_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

    def test_show_flights(self) -> None:
        response = self.client.get(FLIGHT_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_flight(self) -> None:
        route = Route.objects.create(
            source=Airport.objects.create(
                name="test",
                city=City.objects.create(name="test", is_capital=True)
            ),
            destination=Airport.objects.create(
                name="test1",
                city=City.objects.create(name="test1", is_capital=True)
            ),
            distance=100
        )
        flight = {
            "crews": [
                Crew.objects.create(
                    first_name="test",
                    last_name="test",
                    position=Position.objects.create(name="test")
                ),
            ],
            "route": route,
            "airplane": Airplane.objects.create(
                name="test",
                rows=10,
                seats_in_row=10,
                airplane_type=AirplaneType.objects.create(name="test")
            ),
            "departure_time": "2023-07-28T12:02:00Z",
            "arrival_time": "2023-08-28T12:02:00Z"
        }

        response = self.client.post(FLIGHT_URL, flight)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_can_create_flight(self) -> None:
        route = Route.objects.create(
            source=Airport.objects.create(
                name="test",
                city=City.objects.create(name="test", is_capital=True)
            ),
            destination=Airport.objects.create(
                name="test1",
                city=City.objects.create(name="test1", is_capital=True)
            ),
            distance=100
        )
        flight = {
            "crews": [
                Crew.objects.create(
                    first_name="test",
                    last_name="test",
                    position=Position.objects.create(name="test")
                ).id,
                Crew.objects.create(
                    first_name="test1",
                    last_name="test2",
                    position=Position.objects.create(name="test1")
                ).id,
            ],
            "route": route.id,
            "airplane": Airplane.objects.create(
                name="test",
                rows=10,
                seats_in_row=10,
                airplane_type=AirplaneType.objects.create(name="test")
            ).id,
            "departure_time": datetime.now(),
            "arrival_time": datetime.now()
        }

        response = self.client.post(FLIGHT_URL, flight)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
