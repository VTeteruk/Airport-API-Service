from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from crews.models import Position, Crew

CREWS_URL = reverse("crews:crew-list")


class UnauthenticatedCrewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(CREWS_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCrewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

        self.position = Position.objects.create(name="test")

    def test_show_crews(self) -> None:
        response = self.client.get(CREWS_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_crew(self) -> None:
        crew = {
            "first_name": "test",
            "last_name": "test",
            "position": self.position
        }

        response = self.client.post(CREWS_URL, crew)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filtering_by_first_name(self) -> None:
        Crew.objects.create(
            first_name="A",
            last_name="A",
            position=self.position
        )
        Crew.objects.create(
            first_name="B",
            last_name="B",
            position=self.position
        )

        response = self.client.get(CREWS_URL + "?first_name=B")
        self.assertEquals(len(response.data["results"]), 1)

    def test_filtering_by_last_name(self) -> None:
        Crew.objects.create(
            first_name="A",
            last_name="A",
            position=self.position
        )
        Crew.objects.create(
            first_name="B",
            last_name="B",
            position=self.position
        )

        response = self.client.get(CREWS_URL + "?last_name=B")
        self.assertEquals(len(response.data["results"]), 1)

    def test_filtering_by_position(self) -> None:
        Crew.objects.create(
            first_name="A",
            last_name="A",
            position=self.position
        )
        Crew.objects.create(
            first_name="B",
            last_name="B",
            position=Position.objects.create(name="B")
        )

        response = self.client.get(CREWS_URL + "?position=B")
        self.assertEquals(len(response.data["results"]), 1)


class AdminCrewTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.position = Position.objects.create(name="test")

    def test_can_create_crew(self) -> None:
        crew = {
            "first_name": "test",
            "last_name": "test",
            "position": self.position
        }

        response = self.client.post(CREWS_URL, crew)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
