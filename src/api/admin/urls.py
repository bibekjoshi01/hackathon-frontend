from django.urls import include, path

app_label = ["admin"]

urlpatterns = [
    path("user-app/", include("src.user.urls")),
]
