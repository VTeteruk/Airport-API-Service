from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from airplanes.models import AirplaneType, Airplane
from flights.models import Route, Airport, City, Flight

TICKET_URL = reverse("tickets:order-list")


class UnauthenticatedTicketTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(TICKET_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedTicketTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456",
        )
        self.client.force_authenticate(self.user)

    def test_show_tickets(self) -> None:
        response = self.client.get(TICKET_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_create_unique_ticket(self) -> None:
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
        flight = Flight.objects.create(
            route=route,
            airplane=Airplane.objects.create(
                name="test",
                rows=10,
                seats_in_row=10,
                airplane_type=AirplaneType.objects.create(name="test")
            ),
            departure_time=datetime.now(),
            arrival_time=datetime.now()
        )

        ticket = {
          "tickets": [
            {
              "row": 3,
              "seat": 1,
              "flight": flight.id
            }
          ]
        }

        response = self.client.post(TICKET_URL, ticket, format="json")
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(TICKET_URL, ticket, format="json")
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
