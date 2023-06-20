from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("namespace", GroupeffectNamespaceModelViewSet, basename="namespace")

urlpatterns = router.urls
