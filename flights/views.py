from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from airport_service_api.permissions import IsAdminOrReadOnly
from flights.models import City, Airport, Route, Flight
from flights.serializers import CitySerializer, AirportSerializer, \
    RouteSerializer, FlightListSerializer, FlightSerializer


class CityView(ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class AirportView(ModelViewSet):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class RouteView(ModelViewSet):
    serializer_class = RouteSerializer
    queryset = Route.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)


class FlightListView(generics.ListAPIView):
    serializer_class = FlightListSerializer
    queryset = Flight.objects.all()
    permission_classes = (IsAuthenticated,)


class FlightCreateView(generics.CreateAPIView):
    serializer_class = FlightSerializer
    queryset = Flight.objects.all()
    permission_classes = (IsAdminUser,)


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flight.objects.all()
    permission_classes = (IsAdminUser,)
    serializer_class = FlightSerializer
