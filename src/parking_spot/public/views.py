from rest_framework import generics
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.db.models import Q, Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.parking_spot.constants import FEATURE_CHOICES, VEHICLE_TYPES
from .serializers import (
    BookingCreateSerializer,
    ParkingSpotListSerializer,
    ParkingSpotDetailSerializer,
    ParkingSpotReviewCreateSerializer,
)
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Booking, ParkingSpot, ParkingSpotReview


class ParkingSpotFilter(filters.FilterSet):
    vehicle_types = filters.MultipleChoiceFilter(
        choices=VEHICLE_TYPES, method="filter_by_vehicle_types", label="Vehicle Types"
    )
    features = filters.MultipleChoiceFilter(
        choices=FEATURE_CHOICES, method="filter_by_features", label="Features"
    )

    class Meta:
        model = ParkingSpot
        fields = ["vehicle_types", "features"]

    def filter_by_vehicle_types(self, queryset, name, value):
        """
        Custom filter to return parking spots with the given vehicle type.
        """
        # FIXME filter by available capacity
        # return queryset.filter(
        #     Q(vehicles_capacity__vehicle_type=value)
        #     & Q(vehicles_capacity__capacity__gt=0)
        # )
        for vehicle_type in value:
            queryset = queryset.filter(vehicles_capacity__vehicle_type=vehicle_type)

        return queryset.distinct()

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
            return queryset
            # try:
            #     latitude = float(latitude)
            #     longitude = float(longitude)

            #     # Haversine Formula for calculating distance
            #     queryset = queryset.annotate(distance=5.5)

            # except ValueError:
            #     pass

        return queryset


class ParkingSpotRetrieveAPIView(generics.RetrieveAPIView):
    queryset = ParkingSpot.objects.filter(is_active=True)
    serializer_class = ParkingSpotDetailSerializer
    lookup_field = "uuid"


class SearchSuggestionsAPIView(APIView):
    """
    API endpoint to provide search suggestions for parking spots.

    This endpoint accepts a query parameter `search` and returns a list of suggestions
    based on matches with parking spot names, addresses, or postcodes. The results
    are filtered to include only active parking spots and limited to the top 10 matches.

    Query Parameters:
        search (str): The search input provided by the user to filter parking spots.
                      Partial matches are supported for names, addresses, and postcodes.

    Example Request:
        GET /api/v1/public/parking-app/search-suggestions?search=park

    Example Response:
        HTTP 200 OK
        {
            "suggestions": [
                "Green Park, London",
                "Central Parking, New York"
            ]
        }

    Response:
        - suggestions (list): A list of up to 10 suggested matches based on the search query.
          Each suggestion is represented as a string containing the parking spot's address
          or name.

    Notes:
        - The search query is case-insensitive.
        - Results are filtered to ensure only active parking spots are included.
        - If no matches are found, the `suggestions` list will be empty.

    Returns:
        Response: A JSON response with the matching suggestions.
    """

    def get(self, request, *args, **kwargs):
        query = request.query_params.get("search", "").strip()
        suggestions = []

        if query:
            # Filter ParkingSpot objects based on name, address, or postcode
            matches = ParkingSpot.objects.filter(
                Q(name__icontains=query)
                | Q(address__icontains=query)
                | Q(postcode__icontains=query),
                is_active=True,
            ).values("address", "name")[
                :10
            ]  # Limit to top 10 results

            # Format suggestions as an array of addresses
            suggestions = list({match["address"].strip().lower() for match in matches})

        return Response({"suggestions": suggestions})


class ParkingSpotReviewCreateAPIView(generics.CreateAPIView):
    queryset = ParkingSpotReview.objects.all()
    serializer_class = ParkingSpotReviewCreateSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
        return super().perform_create(serializer)


class BookingCreateAPIView(generics.CreateAPIView):
    """
    API endpoint for creating a new booking.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(user=request.user)
            return Response(
                {
                    "message": "Booking created successfully.",
                    "booking_no": booking.booking_no,
                    "status": booking.status,
                    "start_time": booking.start_time,
                    "end_time": booking.end_time,
                    "payment_status": booking.payment_status,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
