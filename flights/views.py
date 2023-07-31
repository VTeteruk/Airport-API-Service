from django.db.migrations import serializer
from django.db.models import F, Count, QuerySet
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from airport_service_api.permissions import IsAdminOrReadOnly
from flights.models import City, Airport, Route, Flight
from flights.serializers import (
    CitySerializer,
    AirportSerializer,
    RouteSerializer,
    FlightSerializer,
    FlightDetailSerializer
)


class CityView(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        name = self.request.query_params.get("name")
        is_capital = self.request.query_params.get("is_capital")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if is_capital:
            queryset = queryset.filter(is_capital=is_capital)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="is_capital",
                description=(
                        "Filter by is_capital "
                        "(ex. .../?is_capital=(0 or 1) 0-false, 1-true)"
                ),
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirportView(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.select_related("city")
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        name = self.request.query_params.get("name")
        city = self.request.query_params.get("city")

        if name:
            queryset = queryset.filter(name__icontains=name)
        if city:
            queryset = queryset.filter(city__name__icontains=city)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="city",
                description="Filter by city",
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class RouteView(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if source:
            queryset = queryset.filter(source__name__icontains=source)
        if destination:
            queryset = queryset.filter(
                destination__name__icontains=destination
            )
        return queryset.select_related("source", "destination", "source__city", "destination__city")

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                description="Filter by source",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="destination",
                description="Filter by destination",
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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

        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if source:
            queryset = queryset.filter(route__source__name__icontains=source)
        if destination:
            queryset = queryset.filter(
                route__destination__name__icontains=destination
            )
        return queryset.select_related(
            "route__source",
            "route__destination",
            "route__source__city",
            "route__destination__city",
            "airplane__airplane_type",
        ).prefetch_related("crews__position")

    def get_serializer_class(self) -> serializer:
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="source",
                description="Filter by source",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="destination",
                description="Filter by destination",
                required=False,
                type=str,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
