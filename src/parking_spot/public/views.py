from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.db.models import Q, Avg

from src.parking_spot.constants import FEATURE_CHOICES, VEHICLE_TYPES
from .serializers import ParkingSpotListSerializer, ParkingSpotDetailSerializer
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import ParkingSpot


class ParkingSpotFilter(filters.FilterSet):
    vehicle_type = filters.ChoiceFilter(
        choices=VEHICLE_TYPES, method="filter_by_vehicle_type", label="Vehicle Type"
    )
    features = filters.MultipleChoiceFilter(
        choices=FEATURE_CHOICES, method="filter_by_features", label="Features"
    )

    class Meta:
        model = ParkingSpot
        fields = ["vehicle_type"]

    def filter_by_vehicle_type(self, queryset, name, value):
        """
        Custom filter to return parking spots with the given vehicle type.
        """
        # FIXME filter by available capacity
        return queryset.filter(
            Q(vehicles_capacity__vehicle_type=value)
            & Q(vehicles_capacity__capacity__gt=0)
        )

    def filter_by_features(self, queryset, name, value):
        """
        Custom filter to return parking spots that contain all specified features.
        """
        for feature in value:
            queryset = queryset.filter(features__feature=feature)
        return queryset.distinct()


class ParkingSpotListAPIView(generics.ListAPIView):
    queryset = ParkingSpot.objects.filter(is_active=True).annotate(
        average_rating=Avg("reviews__rating")
    )
    serializer_class = ParkingSpotListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ParkingSpotFilter
    ordering_fields = ["rate_per_hour", "average_rating", "distance"]
    ordering = ["name"]
    search_fields = ["name", "address", "postcode"]

    def get_queryset(self):
        """
        Overrides the queryset to calculate distance based on query params.
        """
        queryset = super().get_queryset()
        latitude = self.request.query_params.get("latitude")
        longitude = self.request.query_params.get("longitude")

        if latitude and longitude:
            try:
                latitude = float(latitude)
                longitude = float(longitude)

                # Haversine Formula for calculating distance
                queryset = queryset.annotate(distance=5.5)

            except ValueError:
                pass

        return queryset


class ParkingSpotRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ParkingSpot.objects.filter(is_active=True)
    serializer_class = ParkingSpotDetailSerializer
    lookup_field = "uuid"
