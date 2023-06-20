from rest_framework import serializers


class GroupeffectNamespaceModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupeffectNamespace
        fields = "__all__"
