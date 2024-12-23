from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

# Unregister the blacklisted and outstanding token models
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "email",
        "username",
        "full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
        "auth_provider",
    )
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "auth_provider",
        "is_email_verified",
        "is_phone_verified",
    )
    search_fields = ("email", "username", "first_name", "last_name", "phone_no")
    ordering = ("-date_joined",)

    fieldsets = (
        (
            _("Personal Info"),
            {"fields": ("email", "username", "full_name", "phone_no")},
        ),
        (_("Profile"), {"fields": ("photo", "bio", "auth_provider")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("date_joined", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )

    readonly_fields = ("date_joined", "updated_at")
    filter_horizontal = ("groups", "user_permissions")

    def full_name(self, obj):
        return obj.full_name or "N/A"

    full_name.short_description = "Full Name"


# Register the customized UserAdmin
admin.site.register(User, UserAdmin)
