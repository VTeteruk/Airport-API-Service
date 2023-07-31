from django.db import transaction
from rest_framework import serializers

from tickets.models import Order, Ticket


class TicketSerializer(serializers.ModelSerializer):
    # DRY
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs)
        Ticket.validate_seat_and_row(
            attrs["seat"],
            attrs["flight"].airplane.seats_in_row,
            attrs["row"],
            attrs["flight"].airplane.rows,
            serializers.ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderListSerializer(serializers.ModelSerializer):
    tickets = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "created_at", "tickets")

    def create(self, validated_data) -> Order:
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order

    def to_representation(self, instance):
        return OrderListSerializer(instance).data
