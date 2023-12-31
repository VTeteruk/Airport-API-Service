from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.viewsets import ModelViewSet
from tickets.models import Order
from tickets.serializers import OrderSerializer


class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self) -> Order:
        queryset = Order.objects.filter(user=self.request.user)
        source = self.request.query_params.get("source")
        destination = self.request.query_params.get("destination")

        if source:
            queryset = queryset.filter(
                tickets__flight__route__source__name__icontains=source
            )
        if destination:
            queryset = queryset.filter(
                tickets__flight__route__destination__name__icontains=destination
            )

        return queryset.prefetch_related(
                "tickets__flight__route__source", "tickets__flight__route__destination"
            )

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

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
