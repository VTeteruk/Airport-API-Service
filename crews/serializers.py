from rest_framework import serializers
from crews.models import Position, Crew


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    position = serializers.SlugRelatedField(
        slug_field="name", queryset=Position.objects.all()
    )

    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "position")
