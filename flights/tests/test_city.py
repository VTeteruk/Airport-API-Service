from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

CITY_URL = reverse("flights:city-list")


class UnauthenticatedCityTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(CITY_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCityTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

    def test_show_city(self) -> None:
        response = self.client.get(CITY_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_city(self) -> None:
        city = {
            "name": "test",
            "is_capital": True
        }

        response = self.client.post(CITY_URL, city)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminCityTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_can_create_city(self) -> None:
        city = {
            "name": "test",
            "is_capital": True
        }

        response = self.client.post(CITY_URL, city)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
