from django.urls import path

from .views import PublicPostCreateAPIView

urlpatterns = [
    path("posts/create", PublicPostCreateAPIView.as_view())
]
