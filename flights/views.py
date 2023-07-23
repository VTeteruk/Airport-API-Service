from django.db.migrations import serializer
from django.db.models import F, Count, QuerySet
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

    def get_serializer_class(self) -> serializer:
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
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .select_related("airplane")
                .annotate(
                    seats_available=F(
                        "airplane__rows"
                    ) * F("airplane__seats_in_row") - Count("tickets")
                )
            ).order_by("id")
        return queryset

    def get_serializer_class(self) -> serializer:
        if self.action == "retrieve":
            return FlightDetailSerializer
        if self.request.method == "GET":
            return FlightListSerializer
        return FlightSerializer
