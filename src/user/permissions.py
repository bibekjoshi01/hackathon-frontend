from rest_framework.permissions import BasePermission

from src.libs.permissions import validate_permissions


class UserSetupPermission(BasePermission):
    def has_permission(self, request, view):
        user_permissions_dict = {
            "SAFE_METHODS": "view_user",
            "POST": "add_user",
            "PATCH": "edit_user",
            "DELETE": "delete_user",
        }

        return validate_permissions(request, user_permissions_dict)


class UserRoleSetupPermission(BasePermission):
    def has_permission(self, request, view):
        user_permissions_dict = {
            "SAFE_METHODS": "view_user_role",
            "POST": "add_user_role",
            "PATCH": "edit_user_role",
            "DELETE": "delete_user_role",
        }

        return validate_permissions(request, user_permissions_dict)
