from django.contrib import admin
from flights.models import City, Airport, Route, Flight


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_filter = ("name", "is_capital")
    search_fields = ("name",)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_filter = ("source", "destination")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_filter = ("crews", "departure_time", "arrival_time")
