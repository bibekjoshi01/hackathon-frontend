from django.urls import include, path

app_label = ["admin"]

urlpatterns = [
    path("product-app/", include("src.product.urls")),
    path("user-app/", include("src.user.urls")),
]
