from rest_framework import serializers
from flights.models import City, Airport, Route, Flight


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "is_capital")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class AirportListSerializer(serializers.ModelSerializer):
    city = serializers.StringRelatedField()

    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


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


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField()
    crews = serializers.StringRelatedField(many=True)
    airplane = serializers.StringRelatedField()

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
