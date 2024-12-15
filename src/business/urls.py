from django.urls import path
from .views import (
    BusinessCategoryListAPIView,
    BusinessInfoCreateAPIView,
    BusinessInfoListAPIView,
    BusinessInfoRetrieveAPIView,
    BusinessInfoUpdateAPIView,
    SubmitBusinessKYCAPIView,
)

urlpatterns = [
    path(
        "business-info/create",
        BusinessInfoCreateAPIView.as_view(),
        name="business-info-create",
    ),
    path(
        "business-info/update",
        BusinessInfoUpdateAPIView.as_view(),
        name="business-info-update",
    ),
    path(
        "business-info",
        BusinessInfoRetrieveAPIView.as_view(),
        name="business-info-update",
    ),
    path(
        "business-info/<int:farmer_id>",
        BusinessInfoListAPIView.as_view(),
        name="business-info-detail",
    ),
    path(
        "business-info/verify",
        SubmitBusinessKYCAPIView.as_view(),
        name="submit-business-kyc",
    ),
    path("categories", BusinessCategoryListAPIView.as_view()),
]
