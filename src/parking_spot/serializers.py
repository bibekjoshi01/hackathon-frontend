from rest_framework import serializers

from src.base.serializers import AbstractInfoRetrieveSerializer
from src.libs.get_context import get_user_by_context

from .models import (
    ParkingSpot,
    ParkingSpotAvailability,
    ParkingSpotFeatures,
    ParkingSpotReview,
    ParkingSpotVehicleCapacity,
)


class ParkingSpotAvailabilitySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = ParkingSpotAvailability
        fields = ["id", "day", "start_time", "end_time"]


class ParkingSpotVehicleSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = ParkingSpotVehicleCapacity
        fields = ["id", "vehicle_type", "capacity"]


class ParkingSpotFeatureSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = ParkingSpotFeatures
        fields = ["id", "feature"]


class ParkingSpotReviewSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    
    class Meta:
        model = ParkingSpotReview
        fields = ["id", "reviewer", "rating", "comments"]


class ParkingSpotListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSpot
        fields = [
            "id",
            "name",
            "cover_image",
            "address",
            "postcode",
            "rate_per_hour",
            "rate_per_day",
        ]


class ParkingSpotDetailSerializer(AbstractInfoRetrieveSerializer):
    availabilities = ParkingSpotAvailabilitySerializer(many=True)
    features = ParkingSpotFeatureSerializer(many=True)
    vehicles_capacity = ParkingSpotVehicleSerializer(many=True)
    reviews = ParkingSpotReviewSerializer(many=True)

    class Meta(AbstractInfoRetrieveSerializer.Meta):
        model = ParkingSpot
        fields = [
            "id",
            "name",
            "cover_image",
            "address",
            "postcode",
            "description",
            "latitude",
            "longitude",
            "rate_per_hour",
            "rate_per_day",
            "availabilities",
            "features",
            "vehicles_capacity",
            "reviews",
        ]
        fields += AbstractInfoRetrieveSerializer.Meta.fields


class ParkingSpotCreateSerializer(serializers.ModelSerializer):
    availabilities = ParkingSpotAvailabilitySerializer(many=True, allow_null=True)
    features = ParkingSpotFeatureSerializer(many=True, allow_null=True)
    vehicles_capacity = ParkingSpotVehicleSerializer(many=True, allow_null=True)

    class Meta:
        model = ParkingSpot
        fields = [
            "name",
            "cover_image",
            "address",
            "postcode",
            "description",
            "latitude",
            "longitude",
            "rate_per_hour",
            "rate_per_day",
            "availabilities",
            "features",
            "vehicles_capacity",
        ]

    def create(self, validated_data):
        created_by = get_user_by_context(self.context)
        availabilities = validated_data.pop("availabilities", [])
        features = validated_data.pop("features", [])
        vehicles_capacity = validated_data.pop("vehicles_capacity", [])

        parking_spot = ParkingSpot.objects.create(
            owner=created_by, created_by=created_by, **validated_data
        )
        
        for availability in availabilities:
            ParkingSpotAvailability.objects.create(parking_spot=parking_spot, **availability)
        
        for feature in features:
            ParkingSpotFeatures.objects.create(parking_spot=parking_spot, **feature)
        
        for vehicle_capacity in vehicles_capacity:
            ParkingSpotVehicleCapacity.objects.create(parking_spot=parking_spot, **vehicle_capacity)
            
        return parking_spot

    def to_representation(self, instance: ParkingSpot):
        data = super(ParkingSpotCreateSerializer, self).to_representation(instance)
        data["type"] = "success"
        data["message"] = "Parking Spot created successfully."
        data["id"] = instance.id
        return data


class ParkingSpotUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = [
            "name",
            "cover_image",
            "address",
            "postcode",
            "description",
            "latitude",
            "longitude",
            "rate_per_hour",
            "rate_per_day",
        ]

    def update(self, instance: ParkingSpot, validated_data) -> ParkingSpot:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance

    def to_representation(self, instance: ParkingSpot):
        return {
            "type": "success",
            "message": "Parking Spot updated successfully.",
            "id": instance.id,
        }
