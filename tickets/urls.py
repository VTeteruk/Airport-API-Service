from rest_framework import routers
from tickets.views import OrderView

router = routers.SimpleRouter()
router.register("", OrderView)

urlpatterns = router.urls

app_name = "tickets"
