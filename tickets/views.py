from rest_framework.viewsets import ModelViewSet
from tickets.models import Order
from tickets.serializers import OrderSerializer, OrderListSerializer


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

        return queryset

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrderListSerializer
        return OrderSerializer
