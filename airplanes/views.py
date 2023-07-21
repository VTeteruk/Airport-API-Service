from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from airplanes.models import Airplane, AirplaneType
from airplanes.serializers import AirplaneSerializer, AirplaneTypeSerializer
from airport_service_api.permissions import IsAdminOrReadOnly


class AirplaneView(ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)


class AirplaneTypeView(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
