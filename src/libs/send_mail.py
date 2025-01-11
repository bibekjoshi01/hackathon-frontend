import logging

from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.templatetags.static import static

# logger setup for email logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = logging.FileHandler("logs/email_logs.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_basic_urls(request):
    """
    Utility function to generate basic URLs using the current site information.
    """
    current_site = get_current_site(request)
    origin_url = request.headers.get("origin")
    domain = current_site.domain
    base_static_url = f'https://{domain}{static("images/")}'

    # Constructing URLs
    logo = f"{base_static_url}logo.jpeg"
    facebook_icon = f"{base_static_url}icons/facebook.png"
    instagram_icon = f"{base_static_url}icons/instagram.png"
    linkedin_icon = f"{base_static_url}icons/linkedin.png"
    twitter_icon = f"{base_static_url}icons/twitter.png"

    return {
        "origin_url": origin_url,
        "logo": logo,
        "facebook_icon": facebook_icon,
        "instagram_icon": instagram_icon,
        "linkedin_icon": linkedin_icon,
        "twitter_icon": twitter_icon,
    }


def _send_email(subject, body, template_name, context, recipient_email):

    email_template = render_to_string(
        f"user/account_verification.html",
        context={
            "context": context,
        },
    )
    mail = EmailMultiAlternatives(
        subject,
        body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )

    if email_template:
        mail.attach_alternative(email_template, "text/html")

    try:
        mail.send(fail_silently=False)
    except Exception:
        logger.exception("Failed to send email to %s", recipient_email)
        return False
    return True
