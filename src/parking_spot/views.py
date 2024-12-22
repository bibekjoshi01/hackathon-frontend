from django_filters.filterset import FilterSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from src.parking_spot.serializers import (
    ParkingSpotCreateSerializer,
    ParkingSpotDetailSerializer,
    ParkingSpotListSerializer,
    ParkingSpotUpdateSerializer,
)


from .models import ParkingSpot


class FilterForParkingSpotViewSet(FilterSet):
    """Filters for Parking Spot View Set."""

    class Meta:
        model = ParkingSpot
        fields = ["name", "postcode", "rate_per_hour"]


class ParkingSpotViewSet(ModelViewSet):
    """
    Retrieve, create, update, or list parking spots.
    This API supports filtering, searching, and ordering of parking spots.
    """

    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = FilterForParkingSpotViewSet
    search_fields = ["name", "address", "description"]
    ordering = ["-created_at"]
    ordering_fields = ["name", "created_at"]
    http_method_names = ["options", "head", "get", "post", "patch"]

    def get_queryset(self):
        return ParkingSpot.objects.filter(is_archived=False, owner=self.request.user)

    def get_serializer_class(self):
        serializer_class = ParkingSpotListSerializer
        if self.request.method == "GET":
            if self.action == "list":
                serializer_class = ParkingSpotListSerializer
            else:
                serializer_class = ParkingSpotDetailSerializer
        if self.request.method == "POST":
            serializer_class = ParkingSpotCreateSerializer
        if self.request.method == "PATCH":
            serializer_class = ParkingSpotUpdateSerializer

        return serializer_class
