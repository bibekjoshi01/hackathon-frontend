from django.contrib import admin
from . models import ParkingSpot, ParkingSpotAvailability, ParkingSpotFeatures, ParkingSpotReview, ParkingSpotVehicleCapacity

admin.site.register(ParkingSpot)
admin.site.register(ParkingSpotAvailability)
admin.site.register(ParkingSpotFeatures)
admin.site.register(ParkingSpotReview)
admin.site.register(ParkingSpotVehicleCapacity)