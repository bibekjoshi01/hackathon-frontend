from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from . models import ParkingSpot

class ParkingSpotAdmin(admin.ModelAdmin):
    model = ParkingSpot
    list_display = (
        "name",
        "owner",
        "address",
        "created_at",
        "updated_at",
        "is_active",
        "action_buttons",
    )
    
    search_fields = ["name"]
    readonly_fields = ("created_at", "updated_at")
    exclude = ["created_by", "updated_by", "is_archived"]

    def action_buttons(self, obj):
        edit_url = reverse("admin:parking_spot_parkingspot_change", args=[obj.id])
        return format_html(
            '<a class="button" href="{}">'
            '<i class="fas fa-eye"></i>View</a>',
            edit_url,
        )
    
    action_buttons.short_description = "Actions"
    action_buttons.allow_tags = True

    def owner(self, obj):
        return obj.owner.get_full_name() or obj.owner.username
    
    def address(self, obj):
        return obj.address[:50] or "N/A"

    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    

admin.site.register(ParkingSpot, ParkingSpotAdmin)