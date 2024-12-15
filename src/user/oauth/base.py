from typing import Dict
from django.conf import settings


class OAuthProvider:
    """
    Base class for OAuth providers.
    """

    @staticmethod
    def _get_provider_settings(provider_name: str) -> Dict[str, str]:
        """
        Retrieves the OAuth provider settings.

        Returns:
            Dict[str, str]: The provider settings containing client_id and client_secret.

        Raises:
            ValueError: If the provider settings are not found or invalid.
        """

        provider_settings = settings.OAUTH_PROVIDERS.get(provider_name, {})

        if not provider_settings:
            raise ValueError(
                f"{provider_name.capitalize()} OAuth settings are not configured in settings.OAUTH_PROVIDERS.")

        if not provider_settings.get("client_id") or not provider_settings.get("client_secret"):
            raise ValueError(
                f"{provider_name.capitalize()} OAuth settings must include 'client_id' and 'client_secret'."
            )

        return provider_settings
