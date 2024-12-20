from rest_framework import serializers

from ..models import (
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
            "average_rating"
        ]
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.values_list("rating", flat=True)
        total_reviews = self.get_total_reviews(obj)
        if total_reviews == 0:
            return 0
        total_rating = sum(reviews)
        return total_rating/total_reviews


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
            "average_rating",
            "vehicles_capacity",
            "features",
            "availabilities",
            "reviews"
        ]
    
    def get_total_reviews(self, obj):
        return obj.reviews.count()
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.values_list("rating", flat=True)
        total_reviews = self.get_total_reviews(obj)
        if total_reviews == 0:
            return 0
        total_rating = sum(reviews)
        return total_rating/total_reviews   
    

class ParkingSpotReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpotReview
        fields = ["parking_spot", "rating", "comments"]