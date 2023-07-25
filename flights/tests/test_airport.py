from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from flights.models import City

AIRPORT_URL = reverse("flights:airport-list")


class UnauthenticatedAirportTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(AIRPORT_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

        self.city = City.objects.create(name="test", is_capital=True)

    def test_show_airport(self) -> None:
        response = self.client.get(AIRPORT_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_airport(self) -> None:
        airport = {
            "name": "test",
            "city": self.city.id
        }

        response = self.client.post(AIRPORT_URL, airport)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.city = City.objects.create(name="test", is_capital=False)

    def test_can_create_airplane(self) -> None:
        airport = {
            "name": "new_airplane",
            "city": self.city.id
        }

        response = self.client.post(AIRPORT_URL, airport)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
