from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import ParkingSpotViewSet

router = DefaultRouter(trailing_slash=False)

router.register(r"parking-spots", ParkingSpotViewSet, basename="parking-spots")

urlpatterns = [*router.urls]
