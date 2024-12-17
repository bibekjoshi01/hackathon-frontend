from django.db import models

from src.base.models import AbstractInfoModel
from django.contrib.auth import get_user_model

from src.parking_spot.constants import DAYS_OF_WEEK, FEATURE_CHOICES, VEHICLE_TYPES

User = get_user_model()


class ParkingSpot(AbstractInfoModel):
    owner = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="parking_spots"
    )
    name = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to="parking_spot", null=True)
    description = models.TextField()
    address = models.CharField(max_length=500, blank=True)
    postcode = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_day = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class ParkingSpotFeatures(models.Model):
    parking_spot = models.ForeignKey(
        ParkingSpot, on_delete=models.CASCADE, related_name="features"
    )
    feature = models.CharField(choices=FEATURE_CHOICES, max_length=100)
    
    def __str__(self):
        return self.feature


class ParkingSpotVehicleCapacity(models.Model):

    parking_spot = models.ForeignKey(
        ParkingSpot, on_delete=models.CASCADE, related_name="vehicles_capacity"
    )
    vehicle_type = models.CharField(choices=VEHICLE_TYPES, max_length=100)
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.parking_spot.name} - {self.vehicle_type}: {self.capacity} available"


class ParkingSpotAvailability(models.Model):
    day = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(help_text="Start time for availability (HH:MM:SS)")
    end_time = models.TimeField(help_text="End time for availability (HH:MM:SS)")

    parking_spot = models.ForeignKey(
        "ParkingSpot", on_delete=models.CASCADE, related_name="availabilities"
    )

    class Meta:
        unique_together = ("day", "parking_spot")
        ordering = ["day", "start_time"]

    def __str__(self):
        return f"{self.parking_spot} available on {self.get_day_display()} from {self.start_time} to {self.end_time}"


class ParkingSpotReview(models.Model):
    parking_spot = models.ForeignKey(
        ParkingSpot, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    comments = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.parking_spot.name} by {self.reviewer.username}"


class Booking(AbstractInfoModel):
    parking_spot = models.ForeignKey(
        ParkingSpot, on_delete=models.CASCADE, related_name="bookings"
    )
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="user_bookings"
    )
    vehicle_no = models.CharField(max_length=50, help_text="registeration no of vehicle")
    vehicle = models.CharField(choices=VEHICLE_TYPES, max_length=100)
    
    def __str__(self):
        return self.vehicle_no
    
