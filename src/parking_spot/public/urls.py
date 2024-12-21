from django.urls import path

from .views import ParkingSpotListAPIView, ParkingSpotRetrieveAPIView, SearchSuggestionsAPIView, ParkingSpotReviewCreateAPIView

urlpatterns = [
    path("parking-spots", ParkingSpotListAPIView.as_view(), name="parking_spots"),
    path(
        "parking-spots/<uuid:uuid>",
        ParkingSpotRetrieveAPIView.as_view(),
        name="parking_spot",
    ),
    path("search-suggestions", SearchSuggestionsAPIView.as_view(), name="search_suggestions"),
    path("parking-spots/create-review", ParkingSpotReviewCreateAPIView.as_view(), name="create_review"),
]
