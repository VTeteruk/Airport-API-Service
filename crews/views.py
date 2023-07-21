from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from crews.models import Position, Crew
from airport_service_api.permissions import IsAdminOrReadOnly
from crews.serializers import PositionSerializer, CrewSerializer


class PositionView(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)


class CrewView(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
