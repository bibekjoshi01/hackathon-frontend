import secrets

from django.contrib.sites.shortcuts import get_current_site
from django.templatetags.static import static
from django.utils import timezone
from rest_framework import serializers

from src.libs.send_mail import _send_email, get_basic_urls
from src.user.models import User, UserAccountVerification


def send_user_account_verification_email(
    recipient_email,
    user_id,
    request,
    redirect_url="verify-account",
):
    current_site = get_current_site(request)
    origin_url = request.headers.get("origin")
    lock_url = f'http://{current_site.domain}{static("images/icons/lock.png")}'

    try:
        user = User.objects.get(id=user_id)
        token = secrets.token_hex(32)
        subject = "Account Verification"
        body = "Account Information"
        email_template_name = "user/account_verification"
        verification_url = f"{origin_url}/{redirect_url}/{token}"
        email_context = {
            "verification_url": verification_url,
            "lock_url": lock_url,
            "basic_urls": get_basic_urls(request),
        }
        sent_successfully = _send_email(
            subject,
            body,
            email_template_name,
            email_context,
            recipient_email,
        )
        if sent_successfully:
            UserAccountVerification.objects.create(
                user=user,
                token=token,
                created_at=timezone.now(),
                is_archived=False,
            )
    except User.DoesNotExist as err:
        raise serializers.ValidationError({"user_id": "user not found"}) from err
    except Exception as err:
        raise serializers.ValidationError({"error": "unknown error occured"}) from err
