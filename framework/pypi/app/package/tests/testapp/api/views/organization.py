from api.views.organization import OrganizationModelSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser


class OrganizationModelViewSet(ModelViewSet):

    serializer_class = OrganizationModelSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.all()
