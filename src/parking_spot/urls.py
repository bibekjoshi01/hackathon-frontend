from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BookingListView,
    BookingStatusUpdateView,
    ParkingSpotAvailabilityDeleteView,
    ParkingSpotFeaturesDeleteView,
    ParkingSpotVehicleCapacityDeleteView,
    ParkingSpotViewSet,
)

router = DefaultRouter(trailing_slash=False)

router.register(r"parking-spots", ParkingSpotViewSet, basename="parking-spots")

urlpatterns = [
    path("bookings", BookingListView.as_view(), name="booking-list"),
    path(
        "bookings/<int:pk>/update-status",
        BookingStatusUpdateView.as_view(),
        name="booking-status-update",
    ),
    path(
        "availability/<int:pk>/delete/",
        ParkingSpotAvailabilityDeleteView.as_view(),
        name="parking-spot-availability-delete",
    ),
    path(
        "vehicle-capacity/<int:pk>/delete/",
        ParkingSpotVehicleCapacityDeleteView.as_view(),
        name="parking-spot-vehicle-capacity-delete",
    ),
    path(
        "features/<int:pk>/delete/",
        ParkingSpotFeaturesDeleteView.as_view(),
        name="parking-spot-features-delete",
    ),
    *router.urls,
]
