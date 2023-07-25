from rest_framework import serializers
from flights.models import City, Airport, Route, Flight


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "is_capital")


class AirportListSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city")

    def to_representation(self, instance):
        return AirportListSerializer(instance).data


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")

    def to_representation(self, instance):
        return RouteListSerializer(instance).data


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField()
    crews = serializers.StringRelatedField(many=True)
    airplane = serializers.StringRelatedField()
    seats_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "crews",
            "airplane",
            "departure_time",
            "arrival_time",
            "seats_available",
        )


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "crews",
            "airplane",
            "departure_time",
            "arrival_time"
        )

    def to_representation(self, instance):
        return FlightListSerializer(instance).data


class FlightDetailSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField()
    crews = serializers.StringRelatedField(many=True)
    airplane = serializers.StringRelatedField()
    taken_seats = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "crews",
            "airplane",
            "departure_time",
            "arrival_time",
            "taken_seats",
        )

    def get_seat_and_row(self, ticket):
        return {"row": ticket.row, "seat": ticket.seat}

    def get_taken_seats(self, flight):
        return [self.get_seat_and_row(ticket) for ticket in
                flight.tickets.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["taken_seats"] = self.get_taken_seats(instance)
        return data
