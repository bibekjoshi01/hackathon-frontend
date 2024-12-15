from rest_framework import serializers

from src.user.models import MainModule, PermissionCategory, UserGroup, UserPermission


class MainModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainModule
        fields = ["id", "name", "codename", "is_active"]
        read_only_fields = ["created_by", "created_at"]


class UserPermissionCategorySerializer(serializers.ModelSerializer):
    main_module_name = serializers.ReadOnlyField(
        source="main_module.name", allow_null=True,
    )

    class Meta:
        model = PermissionCategory
        fields = ["id", "name", "main_module", "main_module_name", "is_active"]
        read_only_fields = ["created_by", "created_at"]


class UserPermissionSerializer(serializers.ModelSerializer):
    permission_category_name = serializers.ReadOnlyField(
        source="permission_category.name",
    )
    main_module = serializers.ReadOnlyField(source="permission_category.main_module.id")
    main_module_name = serializers.ReadOnlyField(
        source="permission_category.main_module.name",
    )

    class Meta:
        model = UserPermission
        fields = [
            "id",
            "name",
            "codename",
            "permission_category",
            "permission_category_name",
            "main_module",
            "main_module_name",
            "is_active",
        ]
        read_only_fields = ["created_by", "created_at"]


class UserGroupForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ["id", "name", "codename", "is_active"]
