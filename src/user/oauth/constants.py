from enum import Enum
from typing import TypedDict, Optional

from django.utils.translation import gettext_lazy as _


class AuthProviders(Enum):
    GOOGLE = "GOOGLE"
    BY_CREDENTIALS = "BY-CREDENTIALS"

    @classmethod
    def choices(cls):
        return [(key.value, _(key.name.capitalize())) for key in cls]

    @classmethod
    def is_valid_provider(cls, provider: str) -> bool:
        """Checks if the given provider is valid in the enum"""
        return provider in cls._value2member_map_


class UserInfo(TypedDict):
    type: str
    first_name: str
    last_name: str
    full_name: str
    photo: Optional[str]  # None or a string (e.g., URL)
    email: str
