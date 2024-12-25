from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    PublicUserForgetPasswordRequestView,
    PublicUserForgetPasswordView,
    PublicUserProfileUpdateView,
    PublicUserSignInAPIView,
    PublicUserSignUpAPIView,
    PublicUserSocialAuthAPIView,
    PublicUserLogoutAPIView,
    PublicUserProfileView,
    PublicUserVerifyAccountAPIView,
)

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    path(
        "users/social/auth",
        PublicUserSocialAuthAPIView.as_view(),
        name="public_user_social_auth",
    ),
    path(
        "users/signin",
        PublicUserSignInAPIView.as_view(),
        name="public_user_signin",
    ),
    path(
        "users/signup",
        PublicUserSignUpAPIView.as_view(),
        name="public_user_signup",
    ),
    path(
        "users/profile/update",
        PublicUserProfileUpdateView.as_view(),
        name="public_user_profile_update",
    ),
    path(
        "users/verify",
        PublicUserVerifyAccountAPIView.as_view(),
        name="public_user_verify",
    ),
    path("users/logout", PublicUserLogoutAPIView.as_view(), name="public_user_logout"),
    path("users/profile", PublicUserProfileView.as_view(), name="public_user_profile"),
    path(
        "users/forget-password-request",
        PublicUserForgetPasswordRequestView.as_view(),
        name="public_user_forget_password_request",
    ),
    path(
        "users/forget-password",
        PublicUserForgetPasswordView.as_view(),
        name="public_user_forget_password",
    ),
    path("", include(router.urls)),
]
