from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    position = models.ForeignKey(
        to=Position, on_delete=models.CASCADE, related_name="crews"
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.position})"
