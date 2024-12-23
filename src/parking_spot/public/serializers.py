from rest_framework import serializers
from django.utils import timezone

from src.parking_spot.utils import generate_booking_no

from ..models import (
    Booking,
    ParkingSpot,
    ParkingSpotAvailability,
    ParkingSpotVehicleCapacity,
    ParkingSpotFeatures,
    ParkingSpotReview,
    ParkingSpotVehicleCapacity,
)

from src.user.models import User


class UserListSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["uuid", "full_name", "photo"]

    def get_full_name(self, obj):
        return obj.full_name


class ParkingSpotListSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = ParkingSpot
        fields = [
            "uuid",
            "name",
            "cover_image",
            "description",
            "address",
            "rate_per_hour",
            "latitude",
            "longitude",
            "postcode",
            "rate_per_day",
            "total_reviews",
            "average_rating",
        ]

    def get_total_reviews(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.values_list("rating", flat=True)
        total_reviews = self.get_total_reviews(obj)
        if total_reviews == 0:
            return 0
        total_rating = sum(reviews)
        return total_rating / total_reviews


class ParkingSpotFeaturesSerializer(serializers.ModelSerializer):
    feature = serializers.CharField(source="get_feature_display")

    class Meta:
        model = ParkingSpotFeatures
        fields = ["feature"]


class ParkingSpotVehicleCapacitySerializer(serializers.ModelSerializer):
    vehicle_type = serializers.CharField(source="get_vehicle_type_display")

    class Meta:
        model = ParkingSpotVehicleCapacity
        fields = ["vehicle_type", "capacity"]


class ParkingSpotAvailabilitySerializer(serializers.ModelSerializer):
    day = serializers.CharField(source="get_day_display")

    class Meta:
        model = ParkingSpotAvailability
        fields = ["day", "start_time", "end_time"]


class ParkingSpotReviewSerializer(serializers.ModelSerializer):
    reviewer = UserListSerializer()

    class Meta:
        model = ParkingSpotReview
        fields = ["reviewer", "rating", "comments", "created_at"]


class ParkingSpotDetailSerializer(serializers.ModelSerializer):
    total_reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    features = ParkingSpotFeaturesSerializer(many=True)
    vehicles_capacity = ParkingSpotVehicleCapacitySerializer(many=True)
    availabilities = ParkingSpotAvailabilitySerializer(many=True)
    reviews = ParkingSpotReviewSerializer(many=True)

    class Meta:
        model = ParkingSpot
        fields = [
            "name",
            "cover_image",
            "description",
            "address",
            "rate_per_hour",
            "rate_per_day",
            "total_reviews",
            "latitude",
            "longitude",
            "average_rating",
            "vehicles_capacity",
            "features",
            "availabilities",
            "reviews",
        ]

    def get_total_reviews(self, obj):
        return obj.reviews.count()

    def get_average_rating(self, obj):
        reviews = obj.reviews.values_list("rating", flat=True)
        total_reviews = self.get_total_reviews(obj)
        if total_reviews == 0:
            return 0
        total_rating = sum(reviews)
        return total_rating / total_reviews


class ParkingSpotReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpotReview
        fields = ["parking_spot", "rating", "comments"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "parking_spot",
            "start_time",
            "end_time",
            "amount",
            "vehicle_no",
            "vehicle",
        ]

    def validate(self, data):
        if not data["parking_spot"].is_active:
            raise serializers.ValidationError(
                "The selected parking spot is not available."
            )

        if data["start_time"] < timezone.now():
            raise serializers.ValidationError("Start time must be in the future.")

        if data["end_time"] <= data["start_time"]:
            raise serializers.ValidationError("End time must be after the start time.")

        parking_spot = data["parking_spot"]
        rate_per_hour = parking_spot.rate_per_hour
        rate_per_day = parking_spot.rate_per_day

        # Calculate the booking duration in hours
        duration_seconds = (data["end_time"] - data["start_time"]).total_seconds()
        duration_hours = duration_seconds / 3600

        # Calculate the expected amount
        if duration_hours <= 24:
            calculated_amount = rate_per_hour * duration_hours
        else:
            calculated_amount = rate_per_day * (duration_hours // 24)
            remaining_hours = duration_hours % 24
            if remaining_hours > 0:
                calculated_amount += rate_per_hour * remaining_hours

        calculated_amount = round(calculated_amount, 2)

        if data["amount"] != calculated_amount:
            raise serializers.ValidationError(
                f"Incorrect amount. The correct amount should be {calculated_amount:.2f}."
            )

        return data

    def create(self, validated_data):
        # Generate a unique booking number
        validated_data["booking_no"] = generate_booking_no(
            validated_data["parking_spot"].id
        )
        return super().create(validated_data)
