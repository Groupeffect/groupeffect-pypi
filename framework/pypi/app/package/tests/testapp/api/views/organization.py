from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from api.serializers.organization import NamespaceModelSerializer

class NamespaceModelViewSet(ModelViewSet):

    serializer_class = NamespaceModelSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
