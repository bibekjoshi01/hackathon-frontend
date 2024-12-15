# Standard Library Imports
from typing import Dict

# Django Imports
from django.core.exceptions import ValidationError

# Third Party Imports
import requests
from requests.exceptions import RequestException

# Custom Imports
from .base import OAuthProvider
from .constants import UserInfo


class MicrosoftOAuth(OAuthProvider):
    """
    Microsoft OAuth provider class for validating authentication tokens
    and retrieving user information.
    """
    TOKEN_INFO_API = "https://www.linkedin.com/oauth/v2/accessToken"
    USER_INFO_API = "https://api.linkedin.com/v2/me"

    @classmethod
    def validate(cls, auth_token: str = None) -> UserInfo | Dict:
        """
        Validates an authentication token and retrieves user information.

        Args:
            auth_token (str): The authentication token to validate.

        Returns:
            dict: A dictionary containing user information or an error message.

        Raises:
            ValueError: If the auth token is missing or invalid.
            RequestException: If there's an issue with the API request.
            KeyError: If the expected fields are missing in the API response.
        """
        if not cls.TOKEN_INFO_API or not cls.USER_INFO_API:
            raise NotImplementedError("Subclasses must define token_info_api and user_info_api.")

        if not auth_token:
            raise ValidationError("Please provide auth token.")

        linkedin_settings = cls._get_provider_settings("microsoft")

        try:
            # Validate the token with the provider's token API
            token_response = requests.get(
                cls.TOKEN_INFO_API, params={
                    "grant_type": "authorization_code",
                    "code": auth_token,
                    "client_id": linkedin_settings.get("client_id"),
                    "client_secret": linkedin_settings.get("client_secret"),
                }, timeout=10
            )
            token_response.raise_for_status()
            token_info = token_response.json()
            access_token = token_info.get("access_token", None)

            if not access_token:
                raise ValueError("Access token not received from LinkedIn.")

            # Retrieve user information
            user_response = requests.get(
                cls.USER_INFO_API,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=10
            )
            user_response.raise_for_status()
            user_info = user_response.json()

            # Format and return user info
            return {
                "type": "success",
                "provider": "LINKEDIN",
                "first_name": user_info.get("localizedFirstName", ""),
                "last_name": user_info.get("localizedLastName", ""),
                "full_name": f"{user_info.get('localizedFirstName', '')} {user_info.get('localizedLastName', '')}".strip(),
                "photo": user_info.get("picture", None),
                "email": user_info.get("email"),
            }

        except RequestException as err:
            raise ValueError(f"Failed to fetch user information from Microsoft API: {err}")
        except Exception as err:
            raise ValueError(f"Unexpected error occurred: {err}")
