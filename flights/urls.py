from django.urls import path
from rest_framework import routers
from flights.views import CityView, AirportView, RouteView, FlightCreateView, \
    FlightListView, FlightDetailView

router = routers.SimpleRouter()
router.register("cities", CityView)
router.register("airports", AirportView)
router.register("routes", RouteView)

urlpatterns = [
    path("", FlightListView.as_view(), name="flight-list"),
    path("create/", FlightCreateView.as_view(), name="flight-create"),
    path("<int:pk>/", FlightDetailView.as_view(), name="flight-detail")
] + router.urls

app_name = "flights"
