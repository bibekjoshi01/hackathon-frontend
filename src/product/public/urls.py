from django.urls import path

from .views import (
    ProductReviewCreateAPIView,
    PublicCategoryListAPIView,
    PublicProductListAPIView,
    PublicProductRetrieveAPIView,
)

urlpatterns = [
    path("products", PublicProductListAPIView.as_view()),
    path(
        "products/<int:id>",
        PublicProductRetrieveAPIView.as_view(),
        name="product-detail",
    ),
    path(
        "product-review/create",
        ProductReviewCreateAPIView.as_view(),
        name="product-review-create",
    ),
    path("categories", PublicCategoryListAPIView.as_view()),
]
