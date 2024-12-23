from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import BookingListView, BookingStatusUpdateView, ParkingSpotViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"parking-spots", ParkingSpotViewSet, basename="parking-spots")

urlpatterns = [
    path("bookings", BookingListView.as_view(), name="booking-list"),
    path(
        "bookings/<int:pk>/update-status",
        BookingStatusUpdateView.as_view(),
        name="booking-status-update",
    ),
    *router.urls,
]
