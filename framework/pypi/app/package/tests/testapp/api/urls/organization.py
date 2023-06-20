from rest_framework.routers import SimpleRouter
from api.views.organization import NamespaceModelViewSet

router = SimpleRouter()
router.register("organization", NamespaceModelViewSet, basename="organization_namespace")

urlpatterns = router.urls
