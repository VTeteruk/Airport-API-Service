from django.contrib.auth import get_user_model
from django.db import models
from flights.models import Flight


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=get_user_model(), on_delete=models.CASCADE, related_name="orders"
    )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        to=Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        to=Order, on_delete=models.CASCADE, related_name="tickets"
    )
