from django_filters.filterset import FilterSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .serializers import BookingSerializer, BookingStatusUpdateSerializer

from src.parking_spot.serializers import (
    BookingSerializer,
    BookingStatusUpdateSerializer,
    ParkingSpotCreateSerializer,
    ParkingSpotDetailSerializer,
    ParkingSpotListSerializer,
    ParkingSpotUpdateSerializer,
)


from .models import Booking, ParkingSpot


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


class BookingListView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter bookings to only show those belonging to the logged-in user (owner).
        This assumes that the 'owner' of the parking spot is associated with the user.
        """
        user = self.request.user
        return Booking.objects.filter(parking_spot__owner=user, is_active=True)


class BookingStatusUpdateView(generics.UpdateAPIView):
    serializer_class = BookingStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Booking.objects.all()

    def get_object(self):
        """
        Override to ensure the owner can only update their own bookings.
        """
        obj = super().get_object()
        if obj.parking_spot.owner != self.request.user:
            raise PermissionDenied("You do not have permission to update this booking.")
        return obj

    def update(self, request, *args, **kwargs):
        """
        Override to handle the update process for status change.
        """
        booking = self.get_object()
        status = request.data.get("status")
        if status not in ["paid", "unpaid"]:
            return Response({"detail": "Invalid status."}, status=400)

        booking.status = status
        booking.save()

        return Response({"detail": "Booking status updated successfully."})
