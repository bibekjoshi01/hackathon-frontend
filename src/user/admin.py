from django.contrib import admin
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
        "avatar",
        "full_name",
        "email",
        "phone_no",
        "username",
        "role",
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
        "user_permissions",
        "password",
    ]
    list_filter = ["is_active", "groups"]
    readonly_fields = ("date_joined", "updated_at", "last_login")
    search_fields = ["email", "phone_no", "username", "full_name"]

    def full_name(self, obj):
        return obj.full_name or "N/A"

    full_name.short_description = "Full Name"

    def avatar(self, obj):
        """
        Displays the user's photo as an avatar in the admin list.
        If no photo is available, a placeholder avatar is shown.
        """
        if obj.photo:
            return format_html(
                '<img src="{}" alt="Avatar" style="width: 40px; height: 40px; border-radius: 50%; object-fit: cover;">',
                obj.photo.url 
            )
        else:
            return format_html(
                '<img src="https://via.placeholder.com/40" alt="No Avatar" style="width: 40px; height: 40px; border-radius: 50%;">'
            )
            
    avatar.short_description = "Photo"

    def action_buttons(self, obj):
        edit_url = reverse("admin:user_user_change", args=[obj.id])
        return format_html(
            '<a class="button" href="{}">'
            '<i class="fas fa-edit"></i> Edit</a>',
            edit_url,
        )

    action_buttons.short_description = "Actions"
    action_buttons.allow_tags = True

    def role(self, obj):
        """
        Returns the user's primary role based on their first group.
        Assumes groups like 'Owner' or 'Driver' exist in the database.
        Styled as a chip for better UI.
        """
        group_name = obj.groups.values_list("name", flat=True).first()
        if group_name:
            return format_html(
                '<span style="display: inline-block; padding: 2px 8px; '
                'font-size: 12px; font-weight: bold; color: white; '
                'background-color: #007bff; border-radius: 12px;">{}</span>',
                group_name
            )
        return format_html(
            '<span style="display: inline-block; padding: 2px 8px; '
            'font-size: 12px; font-weight: bold; color: white; '
            'background-color: #6c757d; border-radius: 12px;">N/A</span>'
        )

    role.short_description = "Role"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True


admin.site.register(User, UserAdmin)
