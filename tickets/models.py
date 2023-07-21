from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.exceptions import ValidationError

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

    class Meta:
        unique_together = ("row", "seat", "flight")

    @staticmethod
    def validate_seat_and_row(
            seat: int,
            seats_in_row: int,
            row: int,
            rows: int,
            error_to_raise
    ):
        if not (
            1 <= seat <= seats_in_row
        ) or not (
            1 <= row <= rows
        ):
            raise error_to_raise(
                "Incorrect value of row or seat"
            )

    def clean(self):
        self.validate_seat_and_row(
            self.seat,
            self.flight.airplane.seats_in_row,
            self.row,
            self.flight.airplane.rows,
            ValidationError
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self) -> str:
        return f"row-{self.row}, seat-{self.seat} ({self.flight.route})"
