from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle

from src.user.public.messages import (
    ACCOUNT_VERIFIED,
    LOGOUT_SUCCESS,
    PROFILE_UPDATED,
    VERIFICATION_EMAIL_SENT,
)
from src.user.public.serializers import (
    # PublicUserLoginSerializer,
    PublicUserLoginSerializer,
    PublicUserLogoutSerializer,
    PublicUserProfileSerializer,
    PublicUserProfileUpdateSerializer,
    # PublicUserProfileSerializer,
    # PublicUserProfileUpdateSerializer,
    PublicUserSocialAuthSerializer,
    PublicUserSignUpSerializer,
    PublicUserVerifyAccountSerializer,
    # PublicUserVerifyAccountSerializer,
)
from src.user.models import User, UserAccountVerification
from .throttling import LoginThrottle
from src.user.utils.verification import send_user_account_verification_email


class PublicUserSocialAuthAPIView(generics.CreateAPIView):
    """Signin User using different third party applications"""

    permission_classes = [AllowAny]
    serializer_class = PublicUserSocialAuthSerializer
    throttle_classes = [AnonRateThrottle]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUserSignUpAPIView(generics.CreateAPIView):
    """
    User SignUp API View.
    """

    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = PublicUserSignUpSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        return super().perform_create(serializer)


class PublicUserSignInAPIView(APIView):
    """User Login API View"""

    permission_classes = [AllowAny]
    throttle_classes = [LoginThrottle]
    serializer_class = PublicUserLoginSerializer

    def handle_verification(self, data, request):
        user_id = data["id"]
        email = data["email"]
        redirect_url = data["redirect_url"]

        verification_request = UserAccountVerification.objects.filter(
            user_id=user_id, is_archived=False
        )
        verification_request.update(is_archived=True)

        send_user_account_verification_email(
            recipient_email=email,
            user_id=user_id,
            request=request,
            redirect_url=redirect_url.strip("/"),
        )

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            if not data["is_email_verified"]:
                self.handle_verification(data, request)
                response_message = VERIFICATION_EMAIL_SENT.format(email=data["email"])
                return Response(
                    {"status": "verify_email", "message": response_message},
                    status=status.HTTP_200_OK,
                )
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUserVerifyAccountAPIView(APIView):
    """User Verify Account View"""

    permission_classes = [AllowAny]
    serializer_class = PublicUserVerifyAccountSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": ACCOUNT_VERIFIED}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUserLogoutAPIView(APIView):
    """User LogOut View"""

    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data,
            context={"request": request},
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message": LOGOUT_SUCCESS}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicUserProfileView(generics.RetrieveAPIView):
    """User Profile View"""

    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserProfileSerializer

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class PublicUserProfileUpdateView(generics.UpdateAPIView):
    """User Profile Update View"""

    permission_classes = [IsAuthenticated]
    serializer_class = PublicUserProfileUpdateSerializer
    http_method_names = ["patch"]

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            serializer.save()
            return Response({"message": PROFILE_UPDATED}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
