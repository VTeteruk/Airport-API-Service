from django.db import models

from airplanes.models import Airplane
from crews.models import Crew


class City(models.Model):
    name = models.CharField(max_length=255)
    is_capital = models.BooleanField()


class Airport(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(
        to=City, on_delete=models.CASCADE, related_name="airports"
    )


class Route(models.Model):
    source = models.ForeignKey(
        to=Airport, on_delete=models.CASCADE, related_name="routes"
    )
    destination = models.ForeignKey(
        to=Airport, on_delete=models.CASCADE, related_name="routes"
    )
    distance = models.IntegerField()


class Flight(models.Model):
    crews = models.ManyToManyField(
        to=Crew, related_name="flights"
    )
    route = models.ForeignKey(
        to=Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        to=Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
