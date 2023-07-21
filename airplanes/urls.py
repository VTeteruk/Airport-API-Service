from rest_framework.routers import SimpleRouter

from airplanes.views import AirplaneView, AirplaneTypeView

router = SimpleRouter()
router.register("types", AirplaneTypeView)
router.register("", AirplaneView)

urlpatterns = router.urls

app_name = "airplanes"
