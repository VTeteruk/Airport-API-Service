from django.contrib import admin
from crews.models import Position, Crew


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    search_fields = ("first_name", "last_name")
    list_filter = ("first_name", "last_name")
