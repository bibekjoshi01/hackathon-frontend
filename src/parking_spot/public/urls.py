from django.urls import path

from .views import ParkingSpotListAPIView, ParkingSpotRetrieveAPIView

urlpatterns = [
    path("parking-spots", ParkingSpotListAPIView.as_view(), name="parking_spots"),
    path("parking-spots/<uuid:uuid>", ParkingSpotRetrieveAPIView.as_view(), name="parking_spot"),
]