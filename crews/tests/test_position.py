from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from crews.models import Position

POSITION_URL = reverse("crews:position-list")


class UnauthenticatedPositionTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(POSITION_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPositionTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

    def test_show_position(self) -> None:
        response = self.client.get(POSITION_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_position(self) -> None:
        position = {"name": "test"}

        response = self.client.post(POSITION_URL, position)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filtering_by_name(self) -> None:
        Position.objects.create(
            name="A"
        )
        Position.objects.create(
            name="B"
        )

        response = self.client.get(POSITION_URL + "?name=B")
        self.assertEquals(len(response.data["results"]), 1)


class AdminPositionTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_can_create_airplane(self) -> None:
        position = {"name": "test"}

        response = self.client.post(POSITION_URL, position)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
