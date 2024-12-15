from django.urls import include, path

app_label = ["public"]

urlpatterns = [
    # path("blog-app/", include("src.blog.public.urls")),
    path("user-app/", include("src.user.public.urls")),
    path("business-app/", include("src.business.urls")),
    path("product-app/", include("src.product.public.urls")),
]
