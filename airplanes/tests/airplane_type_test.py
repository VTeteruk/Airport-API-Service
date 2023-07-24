from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

AIRPLANE_TYPE_URL = reverse("airplanes:airplanetype-list")


class UnauthenticatedAirplaneTypeTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(AIRPLANE_TYPE_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneTypeTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(user=self.user)

    def test_show_airplane_types(self) -> None:
        response = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_airplane_type(self) -> None:
        airplane_type = {"name": "test"}
        response = self.client.post(AIRPLANE_TYPE_URL, airplane_type)

        self.assertEquals(
            response.status_code, status.HTTP_403_FORBIDDEN
        )


class AdminAirplaneTypeTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )

        self.client.force_authenticate(user=self.user)

    def test_can_create_airplane_type(self) -> None:
        airplane_type = {"name": "test"}
        response = self.client.post(AIRPLANE_TYPE_URL, airplane_type)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
