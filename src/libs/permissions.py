from rest_framework.permissions import SAFE_METHODS

from src.user.models import UserRole


def get_user_permissions(request):
    permissions = set()
    user_permissions = []

    user = request.user
    if user.is_anonymous:
        return user_permissions

    groups = UserRole.objects.filter(user=user)

    if groups is not None:
        for group in groups:
            group_permissions = group.permissions.values_list("codename", flat=True)
            permissions.update(set(group_permissions))
        user_permissions = list(permissions)

    return user_permissions


def validate_permissions(request, user_permissions_dict):
    if request.user.is_anonymous:
        return False

    if not request.user.is_active:
        return False

    if request.user.is_superuser:
        return True

    user_permissions = get_user_permissions(request)

    method = request.method
    if method in SAFE_METHODS:
        method = "SAFE_METHODS"

    method_permission = user_permissions_dict.get(method, None)

    if method_permission and method_permission in user_permissions:
        return True

    return False
