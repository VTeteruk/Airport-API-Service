from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from airplanes.models import AirplaneType, Airplane

AIRPLANE_URL = reverse("airplanes:airplane-list")


class UnauthenticatedAirplaneTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(AIRPLANE_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

        self.airplane_type = AirplaneType.objects.create(name="test")

    def test_show_airplanes(self) -> None:
        response = self.client.get(AIRPLANE_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_airplane(self) -> None:
        airplane = {
            "name": "new_airplane",
            "rows": 15,
            "seats_in_row": 10,
            "airplane_type": self.airplane_type
        }

        response = self.client.post(AIRPLANE_URL, airplane)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filtering_by_name(self) -> None:
        Airplane.objects.create(
            name="A",
            rows=1,
            seats_in_row=1,
            airplane_type=self.airplane_type
        )
        Airplane.objects.create(
            name="B",
            rows=1,
            seats_in_row=1,
            airplane_type=self.airplane_type
        )

        response = self.client.get(AIRPLANE_URL + "?name=B")
        self.assertEquals(len(response.data["results"]), 1)


class AdminAirplaneTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.airplane_type = AirplaneType.objects.create(name="test")

    def test_can_create_airplane(self) -> None:
        airplane = {
            "name": "new_airplane",
            "rows": 15,
            "seats_in_row": 10,
            "airplane_type": self.airplane_type
        }

        response = self.client.post(AIRPLANE_URL, airplane)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
