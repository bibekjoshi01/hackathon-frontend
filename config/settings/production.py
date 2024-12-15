# ruff: noqa: E501
import logging

import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .base import *  # noqa: F403
from .base import (
    DATABASES,
    INSTALLED_APPS,
    MIDDLEWARE,
    REDIS_DB,
    REDIS_HOST,
    REDIS_PORT,
    SPECTACULAR_SETTINGS,
    env,
)

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", False)
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["example.com"])

# DATABASES
# ------------------------------------------------------------------------------
DATABASES["default"]["CONN_MAX_AGE"] = env.int("CONN_MAX_AGE", default=60)


# Middlewares
# ------------------------------------------------------------------------------
BLOCK_POSTMAN_REQUEST = env.bool("BLOCK_POSTMAN_REQUEST", True)
if BLOCK_POSTMAN_REQUEST:
    MIDDLEWARE += ["src.libs.middlewares.BlockPostmanMiddleware"]


# CACHES
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "IGNORE_EXCEPTIONS": True,
        },
    },
}

# SECURITY
# ------------------------------------------------------------------------------
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS",
    default=True,
)
SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF",
    default=True,
)

# STATIC & MEDIA
# ------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# EMAIL
# ------------------------------------------------------------------------------
DEFAULT_FROM_EMAIL = env(
    "DEFAULT_FROM_EMAIL",
    default="django_starter <noreply@example.com>",
)
SERVER_EMAIL = env("SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)
EMAIL_SUBJECT_PREFIX = env(
    "DJANGO_EMAIL_SUBJECT_PREFIX",
    default="[Stars of Africa] ",
)

# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("DJANGO_ADMIN_URL")

# Anymail
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["anymail"]
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
ANYMAIL = {}

MIDDLEWARE += ["src.libs.middlewares.BlockPostmanMiddleware"]

# LOGGING
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "../logs/logs.log",
            "formatter": "verbose",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "serializers": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.views": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "sentry_sdk": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console", "file"],
            "propagate": False,
        },
    },
}

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = env("SENTRY_DSN")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send errors as events
)
integrations = [
    sentry_logging,
    DjangoIntegration(),
    CeleryIntegration(),
    RedisIntegration(),
]
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=integrations,
    environment=env("SENTRY_ENVIRONMENT", default="production"),
    traces_sample_rate=env.float("SENTRY_TRACES_SAMPLE_RATE", default=0.0),
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)

# django-rest-framework
# -------------------------------------------------------------------------------
SPECTACULAR_SETTINGS["SERVERS"] = [
    {"url": "https://example.com", "description": "Production server"},
]
