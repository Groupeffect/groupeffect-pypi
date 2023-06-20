from api.serializers.organization import Organization
from rest_framework import serializers


class OrganizationModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
