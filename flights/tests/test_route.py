from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient

from flights.models import Airport, City, Route

ROUTE_URL = reverse("flights:route-list")


class UnauthenticatedRouteTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_have_no_permission(self) -> None:
        response = self.client.get(ROUTE_URL)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRouteTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="123456"
        )
        self.client.force_authenticate(self.user)

        self.airport = Airport.objects.create(
            name="test",
            city=City.objects.create(name="test", is_capital=True)
        )

    def test_show_route(self) -> None:
        response = self.client.get(ROUTE_URL)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_do_not_allow_to_create_route(self) -> None:
        route = {
            "source": self.airport.id,
            "destination": self.airport.id,
            "distance": 1
        }

        response = self.client.post(ROUTE_URL, route)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filtering_by_source(self) -> None:
        Route.objects.create(
            source=Airport.objects.create(
                name="B",
                city=City.objects.create(name="test", is_capital=True)
            ),
            destination=self.airport,
            distance=100
        )
        Route.objects.create(
            source=self.airport,
            destination=self.airport,
            distance=100
        )

        response = self.client.get(ROUTE_URL + "?source=B")
        self.assertEquals(len(response.data["results"]), 1)

    def test_filtering_by_destination(self) -> None:
        Route.objects.create(
            source=self.airport,
            destination=Airport.objects.create(
                name="B",
                city=City.objects.create(name="test", is_capital=True)
            ),
            distance=100
        )
        Route.objects.create(
            source=self.airport,
            destination=self.airport,
            distance=100
        )

        response = self.client.get(ROUTE_URL + "?destination=B")
        self.assertEquals(len(response.data["results"]), 1)


class AdminRouteTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="admin@admin.com",
            password="123456",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

        self.airport = Airport.objects.create(
            name="test",
            city=City.objects.create(name="test", is_capital=True)
        )

    def test_can_create_route(self) -> None:
        route = {
            "source": self.airport.id,
            "destination": self.airport.id,
            "distance": 1
        }

        response = self.client.post(ROUTE_URL, route)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
