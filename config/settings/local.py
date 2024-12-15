# ruff: noqa: E501
from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE, env

# GENERAL
# ------------------------------------------------------------------------------
DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="sydPDD94R0UBhmbBTsXrQ4QDskUY3cPo6cmaa9YorUYNsbzgJqDgnEONnuGpxQ4x",
)
ALLOWED_HOSTS = ['*', "192.168.137.1"]

# WhiteNoise
# ------------------------------------------------------------------------------
INSTALLED_APPS = ["whitenoise.runserver_nostatic", *INSTALLED_APPS]

# django-debug-toolbar
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["debug_toolbar"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": ["debug_toolbar.panels.redirects.RedirectsPanel"],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ["django_extensions"]
