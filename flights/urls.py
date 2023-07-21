from rest_framework import routers
from flights.views import CityView, AirportView, RouteView, FlightView

router = routers.DefaultRouter()
router.register("cities", CityView)
router.register("airports", AirportView)
router.register("routes", RouteView)
router.register("", FlightView)

urlpatterns = router.urls

app_name = "flights"
