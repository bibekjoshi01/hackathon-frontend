from django.urls import include, path

app_label = ["public"]

urlpatterns = [
    path("user-app/", include("src.user.public.urls")),
    path("parking-app/", include("src.parking_spot.public.urls")),
    path("website-app/", include("src.website.urls")),
]
