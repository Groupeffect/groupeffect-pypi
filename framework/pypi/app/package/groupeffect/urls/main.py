from rest_framework.routers import SimpleRouter
from groupeffect.views.main import GroupeffectNamespaceModelViewSet

router = SimpleRouter()
router.register("namespace", GroupeffectNamespaceModelViewSet, basename="namespace")

urlpatterns = router.urls
