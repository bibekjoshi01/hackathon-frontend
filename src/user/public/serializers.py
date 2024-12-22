# Standard Library Imports
from typing import Dict, Union
from datetime import timedelta

# Django Core Imports
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password

# Rest Framework Imports
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

# Custom Imports
from src.user.oauth import AuthTokenValidator, AuthProviders
from src.user.models import User, UserAccountVerification, UserRole
from src.user.utils.generate_username import generate_unique_user_username
from src.user.utils.verification import send_user_account_verification_email
from .messages import (
    ACCOUNT_DISABLED,
    ALREADY_VERIFIED,
    ERROR_MESSAGES,
    INVALID_CREDENTIALS,
    INVALID_LINK,
    INVALID_PASSWORD,
    LINK_EXPIRED,
    LOGIN_SUCCESS,
    PASSWORDS_NOT_MATCH,
    UNKNOWN_ERROR,
    VERIFICATION_EMAIL_SENT,
)


class PublicUserSocialAuthSerializer(serializers.Serializer):
    third_party_app = serializers.ChoiceField(choices=AuthProviders.choices())
    auth_token = serializers.CharField()

    def register_or_login_user(self, user_info: Dict) -> Dict[str, str | int]:
        """
        Registers a new user or logs in an existing one based on the third-party OAuth response.
        """
        try:
            user: User = User.objects.get(email=user_info["email"])

            # Check if account status is active
            if not user.is_active:
                raise serializers.ValidationError(
                    {"message": ERROR_MESSAGES["account_disabled"]}
                )

            if not user.is_email_verified:
                user.is_email_verified = True

        except User.DoesNotExist:
            user = User.objects.create_public_user(
                auth_provider=user_info.get("provider"),
                username=user_info.get("email").split("@")[
                    0
                ],  # Generate username from email
                email=user_info.get("email"),
                password=settings.SOCIAL_SECRET,
                photo=user_info.get("photo"),
                first_name=user_info.get("first_name"),
                last_name=user_info.get("last_name"),
            )

            user.created_by = user

        user.last_login = timezone.now()
        user.save()

        return {"uuid": user.uuid, "tokens": user.tokens, "full_name": user.full_name}

    def validate(self, attrs) -> Dict[str, Union[str, int]]:
        provider = attrs.get("third_party_app", "")
        auth_token = attrs.get("auth_token", "")

        user_info = AuthTokenValidator.validate(provider, auth_token)

        return self.register_or_login_user(user_info)


class PublicUserSignUpSerializer(serializers.ModelSerializer):
    """Public User SignUp Serializer"""

    ACCOUNT_TYPES = (
        ("DRIVER", "Driver"),
        ("OWNER", "Owner"),
    )
    first_name = serializers.CharField(max_length=50, required=True)
    middle_name = serializers.CharField(max_length=50, allow_blank=True, default="cast")
    last_name = serializers.CharField(max_length=50, required=True)
    phone_no = serializers.CharField(max_length=10, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        max_length=16,
        write_only=True,
        min_length=8,
        required=True,
        validators=[validate_password],
    )
    has_accepted_terms = serializers.BooleanField(default=False)
    redirect_url = serializers.CharField(required=True, help_text="verify-account")
    account_type = serializers.ChoiceField(choices=ACCOUNT_TYPES)

    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_no",
            "password",
            "has_accepted_terms",
            "redirect_url",
            "account_type",
        ]

    def validate(self, attrs):
        if not attrs["has_accepted_terms"]:
            raise serializers.ValidationError(
                {"has_accepted_terms": "You must accept our Terms of Service."},
            )

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": ERROR_MESSAGES["email_exists"]})

        if User.objects.filter(phone_no=attrs["phone_no"]).exists():
            raise serializers.ValidationError(
                {"phone_no": ERROR_MESSAGES["phone_exists"]}
            )

        return attrs

    def create(self, validated_data):
        email = validated_data["email"]
        redirect_url = validated_data.pop("redirect_url", None)

        username = generate_unique_user_username(user_type="website_user")

        user_instance = User.objects.create_public_user(
            first_name=validated_data["first_name"].title(),
            middle_name=validated_data.get("middle_name", "").title(),
            last_name=validated_data["last_name"].title(),
            phone_no=validated_data["phone_no"],
            password=validated_data["password"],
            email=email,
            username=username,
        )

        account_type = validated_data.pop("account_type", None)

        if account_type == "DRIVER":
            user_group = UserRole.objects.get(codename="DRIVER")

        elif account_type == "OWNER":
            user_group = UserRole.objects.get(codename="OWNER")

            user_instance.groups.add(user_group)

        user_instance.save()

        send_user_account_verification_email(
            recipient_email=email,
            user_id=user_instance.id,
            request=self.context["request"],
            redirect_url=redirect_url.strip("/"),
        )

        return user_instance

    def to_representation(self, instance):
        return {
            "type": "Account Verification.",
            "message": VERIFICATION_EMAIL_SENT.format(email=instance.email),
        }


class PublicUserLoginSerializer(serializers.ModelSerializer):
    """User Login Serializer"""

    persona = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    redirect_url = serializers.CharField(required=True, help_text="verify-account")

    class Meta:
        model = User
        fields = ["persona", "password", "redirect_url"]

    def validate(self, attrs):
        persona = attrs.get("persona", None)
        password = attrs.pop("password", "")
        redirect_url = attrs.pop("redirect_url", None)

        user = self.get_user(persona)
        self.check_password(user, password)
        self.check_user_status(user)
        # self.check_website_user(user)

        roles = user.groups.filter(is_archived=False, is_active=True).values_list(
            "name", flat=True
        )

        # Update the last login datetime
        user.last_login = timezone.now()
        user.save()

        return {
            "message": LOGIN_SUCCESS,
            "status": "success",
            "id": user.id,
            "uuid": user.uuid,
            "redirect_url": redirect_url,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "phone_no": user.phone_no,
            "is_email_verified": user.is_email_verified,
            "is_phone_verified": user.is_phone_verified,
            "email": user.email,
            "tokens": user.tokens,
            "roles": roles,
        }

    def get_user(self, persona):
        try:
            if "@" in persona:
                user = User.objects.get(email=persona)
            else:
                user = User.objects.get(username=persona)
        except User.DoesNotExist as err:
            raise serializers.ValidationError({"persona": INVALID_CREDENTIALS}) from err
        return user

    def check_website_user(self, user):
        try:
            website_user = UserRole.objects.get(Q(codename="DRIVER") | Q(codename="OWNER"))
        except UserRole.DoesNotExist as err:
            raise serializers.ValidationError({"error": UNKNOWN_ERROR}) from err

        # Fetch all roles associated with the user
        user_roles = user.user_roles.values_list("role", flat=True)

        if website_user.id not in user_roles:
            raise serializers.ValidationError({"persona": INVALID_CREDENTIALS})

    def check_password(self, user, password):
        if not user.check_password(password):
            raise serializers.ValidationError({"password": INVALID_PASSWORD})

    def check_user_status(self, user):
        if not user.is_active or user.is_archived:
            raise serializers.ValidationError({"persona": ACCOUNT_DISABLED})


class PublicUserLogoutSerializer(serializers.Serializer):
    """User Logout Serializer"""

    refresh_token = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={"required": "Refresh token is required."},
    )

    def validate(self, attrs):
        refresh_token = attrs.get("refresh_token", None)
        try:
            RefreshToken(refresh_token)
        except Exception as err:
            raise serializers.ValidationError(
                {"refresh_token": "Invalid Refresh Token"},
            ) from err

        return attrs

    def create(self, validated_data):
        refresh_token = validated_data.get("refresh_token", None)
        try:
            RefreshToken(refresh_token).blacklist()
        except Exception as err:
            error_message = "Invalid Refresh Token"
            raise serializers.ValidationError(error_message) from err
        return validated_data


class PublicUserProfileSerializer(serializers.ModelSerializer):
    """User Profile Serializer"""

    full_name = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "photo",
            "first_name",
            "middle_name",
            "bio",
            "last_name",
            "full_name",
            "phone_no",
            "email",
            "date_joined",
            "is_email_verified",
            "is_phone_verified",
            "roles",
        ]

    def get_full_name(self, obj) -> str:
        return obj.full_name

    def get_roles(self, obj) -> list:
        return list(obj.groups.values_list("name", flat=True))


class PublicUserProfileUpdateSerializer(serializers.ModelSerializer):
    """User Profile Update Serializer"""

    first_name = serializers.CharField(max_length=50, required=False)
    middle_name = serializers.CharField(max_length=50, required=False, allow_blank=True)
    last_name = serializers.CharField(max_length=50, required=False)
    photo = serializers.ImageField(allow_null=True, required=False)
    phone_no = serializers.CharField(max_length=10, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "bio",
            "phone_no",
            "photo",
        ]

    def update(self, instance, validated_data):
        photo = validated_data.get("photo", None)
        user = instance

        # Update user details
        user.first_name = (
            validated_data.get("first_name", user.first_name).strip().title()
        )
        user.middle_name = (
            validated_data.get("middle_name", user.middle_name).strip().title()
        )
        user.last_name = validated_data.get("last_name", user.last_name).strip().title()
        user.bio = validated_data.get("bio", user.bio).strip()

        user.phone_no = validated_data.get("phone_no", user.phone_no)
        user.updated_at = timezone.now()

        if "photo" in validated_data:
            if photo is not None:
                upload_path = user.get_upload_path(
                    upload_path="user/photos",
                    filename=photo.name,
                )
                user.photo.delete(save=False)  # Remove the old file
                user.photo.save(upload_path, photo)
            else:
                user.photo.delete(
                    save=True,
                )  # Delete the existing photo if photo is None

        user.save()
        return user


class PublicUserVerifyAccountSerializer(serializers.Serializer):
    """Public User Verify Account Serializer"""

    token = serializers.CharField(max_length=256, required=True)

    def validate(self, attrs):
        token = attrs.get("token")

        try:
            verification_request = UserAccountVerification.objects.get(
                token=token, is_archived=False
            )
            now = timezone.now()
            delta = now - verification_request.created_at

            if verification_request.user.is_email_verified:
                verification_request.is_archived = True
                verification_request.save()
                raise serializers.ValidationError({"email": ALREADY_VERIFIED})

            if delta > timedelta(minutes=settings.AUTH_LINK_EXP_TIME):
                verification_request.is_archived = True
                verification_request.save()
                raise serializers.ValidationError({"token": LINK_EXPIRED})

        except UserAccountVerification.DoesNotExist as err:
            raise serializers.ValidationError({"token": INVALID_LINK}) from err

        attrs["verification_request"] = verification_request

        return attrs

    def create(self, validated_data):
        verification_request = validated_data["verification_request"]
        user_instance = verification_request.user
        user_instance.is_email_verified = True
        user_instance.save()
        verification_request.is_archived = True
        verification_request.save()
        return validated_data
