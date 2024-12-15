from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import AbstractInfoModel, PublicAbstractInfoModel


class AbstractInfoRetrieveSerializer(ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source="created_by.username")
    created_by_full_name = serializers.SerializerMethodField()

    class Meta:
        model = AbstractInfoModel
        fields = [
            "created_by",
            "created_by_username",
            "created_by_full_name",
            "created_at",
            "updated_at",
            "is_active",
        ]

    def get_created_by_full_name(
        self,
        obj,
    ) -> str:
        return obj.created_by.full_name


class PublicAbstractInfoRetrieveSerializer(ModelSerializer):

    class Meta:
        model = PublicAbstractInfoModel
        fields = ["created_at", "updated_at", "is_active"]
