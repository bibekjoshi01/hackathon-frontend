from django.urls import include, path

app_label = ["admin"]

urlpatterns = [
    path("parking-spot-app/", include("src.parking_spot.urls")),
]
