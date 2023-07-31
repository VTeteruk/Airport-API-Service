from django.contrib import admin
from airplanes.models import AirplaneType, Airplane


@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    list_filter = ("name",)
