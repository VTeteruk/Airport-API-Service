from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255)


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.ForeignKey(
        to=Position, on_delete=models.CASCADE, related_name="crews"
    )
