from rest_framework.viewsets import ModelViewSet
from crews.models import Position, Crew
from crews.serializers import PositionSerializer, CrewSerializer


class PositionView(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class CrewView(ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
