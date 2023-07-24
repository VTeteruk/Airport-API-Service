from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from airplanes.models import Airplane, AirplaneType
from airplanes.serializers import AirplaneSerializer, AirplaneTypeSerializer
from airport_service_api.permissions import IsAdminOrReadOnly


class BaseAirplaneViewSet(ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                description="Filter by name",
                required=False,
                type=str
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class AirplaneView(BaseAirplaneViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer


class AirplaneTypeView(BaseAirplaneViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
