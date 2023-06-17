from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from groupeffect.serializers.main import GroupeffectNamespaceModelSerializer


class GroupeffectNamespaceModelViewSet(ModelViewSet):

    serializer_class = GroupeffectNamespaceModelSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
