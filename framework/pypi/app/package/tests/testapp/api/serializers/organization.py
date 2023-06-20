from rest_framework import serializers
from api.database.organization import Namespace 


class NamespaceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Namespace
        fields = "__all__"
