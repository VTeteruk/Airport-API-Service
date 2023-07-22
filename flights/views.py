from django.db.migrations import serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from airport_service_api.permissions import IsAdminOrReadOnly
from flights.models import City, Airport, Route, Flight
from flights.serializers import (
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    FlightListSerializer,
    FlightSerializer,
    RouteListSerializer,
    AirportListSerializer, FlightDetailSerializer
)


class CityView(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class AirportView(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AirportListSerializer
        return AirportSerializer


class RouteView(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_serializer_class(self) -> serializer:
        if self.request.method == "GET":
            return RouteListSerializer
        return RouteSerializer


class FlightView(ModelViewSet):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FlightDetailSerializer
        if self.request.method == "GET":
            return FlightListSerializer
        return FlightSerializer
