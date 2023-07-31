from rest_framework import routers

from crews.views import PositionView, CrewView

router = routers.SimpleRouter()
router.register("positions", PositionView)
router.register("", CrewView)

urlpatterns = router.urls

app_name = "crews"
