from rest_framework import serializers
from flights.models import City, Airport, Route, Flight


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ("id", "name", "is_capital")


class AirportSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(
        many=False, queryset=City.objects.all(), slug_field="name"
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "city")


class RouteSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(
        many=False, queryset=Airport.objects.all(), slug_field="name"
    )
    destination = serializers.SlugRelatedField(
        many=False, queryset=Airport.objects.all(), slug_field="name"
    )

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
