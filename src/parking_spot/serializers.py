from rest_framework import serializers
from django.db import transaction

from src.base.serializers import AbstractInfoRetrieveSerializer
from src.libs.get_context import get_user_by_context

from .models import (
    Booking,
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
            ParkingSpotAvailability.objects.create(
                parking_spot=parking_spot, **availability
            )

        for feature in features:
            ParkingSpotFeatures.objects.create(parking_spot=parking_spot, **feature)

        for vehicle_capacity in vehicles_capacity:
            ParkingSpotVehicleCapacity.objects.create(
                parking_spot=parking_spot, **vehicle_capacity
            )

        return parking_spot

    def to_representation(self, instance: ParkingSpot):
        data = super(ParkingSpotCreateSerializer, self).to_representation(instance)
        data["type"] = "success"
        data["message"] = "Parking Spot created successfully."
        data["id"] = instance.id
        return data


class ParkingSpotAvailabilityUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=ParkingSpotAvailability.objects.filter(is_active=True),
    )

    class Meta:
        model = ParkingSpotAvailability
        fields = ["id", "day", "start_time", "end_time"]


class ParkingSpotVehicleUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=ParkingSpotVehicleCapacity.objects.filter(is_active=True),
    )

    class Meta:
        model = ParkingSpotVehicleCapacity
        fields = ["id", "vehicle_type", "capacity"]


class ParkingSpotFeatureUpdateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=ParkingSpotFeatures.objects.filter(is_active=True),
    )

    class Meta:
        model = ParkingSpotFeatures
        fields = ["id", "feature"]


class ParkingSpotUpdateSerializer(serializers.ModelSerializer):
    availabilities = ParkingSpotAvailabilityUpdateSerializer(many=True, allow_null=True)
    features = ParkingSpotFeatureUpdateSerializer(many=True, allow_null=True)
    vehicles_capacity = ParkingSpotVehicleUpdateSerializer(many=True, allow_null=True)

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

    def update_related_objects(
        self, instance, data_list, model_class, relation_field_name
    ):
        for data in data_list:
            print(data)
            obj_instance = data.pop("id", None)
            if obj_instance:
                for key, value in data.items():
                    setattr(obj_instance, key, value)
                obj_instance.save()
            else:
                model_class.objects.create(parking_spot=instance, **data)

    def update(self, instance: ParkingSpot, validated_data) -> ParkingSpot:
        availabilities = validated_data.pop("availabilities", [])
        features = validated_data.pop("features", [])
        vehicles_capacity = validated_data.pop("vehicles_capacity", [])
        
        print(features)

        with transaction.atomic():

            for key, value in validated_data.items():
                setattr(instance, key, value)

            instance.save()

            self.update_related_objects(
                instance, availabilities, ParkingSpotAvailability, "availability"
            )
            self.update_related_objects(
                instance, features, ParkingSpotFeatures, "feature"
            )
            self.update_related_objects(
                instance,
                vehicles_capacity,
                ParkingSpotVehicleCapacity,
                "vehicle_capacity",
            )

        return instance

    def to_representation(self, instance: ParkingSpot):
        return {
            "type": "success",
            "message": "Parking Spot updated successfully.",
            "id": instance.id,
        }


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class BookingStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status'] 
