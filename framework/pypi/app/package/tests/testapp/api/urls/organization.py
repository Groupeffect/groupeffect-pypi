from api.urls.organization import OrganizationModelViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("namespace", OrganizationModelViewSet, basename="namespace")

urlpatterns = router.urls
