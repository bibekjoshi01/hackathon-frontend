from django.urls import include, path

app_label = ["public"]

urlpatterns = [
    path("user-app/", include("src.user.public.urls")),
]
