from django.contrib import admin

from .models import (
    PermissionCategory,
    User,
    UserRole,
    UserPermission
)

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(UserPermission)
admin.site.register(PermissionCategory)
