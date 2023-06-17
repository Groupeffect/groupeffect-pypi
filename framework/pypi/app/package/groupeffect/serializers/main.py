from rest_framework import serializers
from groupeffect.database.main import GroupeffectNamespace


class GroupeffectNamespaceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeffectNamespace
        fields = "__all__"
