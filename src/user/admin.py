from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User
from django.urls import reverse
from django.utils.html import format_html

from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

# Unregister the blacklisted and outstanding token models
admin.site.unregister(BlacklistedToken)
admin.site.unregister(OutstandingToken)


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = (
        "photo",
        "full_name",
        "email",
        "phone_no",
        "username",
        "last_login",
        "date_joined",
        "is_active",
        "action_buttons",
    )
    exclude = [
        "uuid",
        "created_at",
        "updated_at",
        "created_by",
        "is_archived",
    ]
    list_filter = []
    readonly_fields = ("date_joined", "updated_at")

    def full_name(self, obj):
        return obj.full_name or "N/A"

    full_name.short_description = "Full Name"

    def action_buttons(self, obj):
        edit_url = reverse("admin:user_user_change", args=[obj.id])
        return format_html(
            '<a class="button" href="{}">'
            '<i class="fas fa-edit"></i> Edit</a>',
            edit_url,
        )

    action_buttons.short_description = "Actions"
    action_buttons.allow_tags = True

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


# Register the customized UserAdmin
admin.site.register(User, UserAdmin)
