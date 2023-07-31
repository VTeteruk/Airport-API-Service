from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from crews.models import Position, Crew
from airport_service_api.permissions import IsAdminOrReadOnly
from crews.serializers import PositionSerializer, CrewSerializer


class PositionView(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
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
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CrewView(ModelViewSet):
    queryset = Crew.objects.select_related("position")
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        position = self.request.query_params.get("position")
        first_name = self.request.query_params.get("first_name")
        last_name = self.request.query_params.get("last_name")

        if position:
            queryset = queryset.filter(position__name__icontains=position)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="position",
                description="Filter by position",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="first_name",
                description="Filter by first_name",
                required=False,
                type=str
            ),
            OpenApiParameter(
                name="last_name",
                description="Filter by last_name",
                required=False,
                type=str
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
