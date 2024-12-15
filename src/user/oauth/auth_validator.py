from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import APIException

# Custom Imports
from .constants import AuthProviders, UserInfo
from .messages import ERROR_MESSAGES
from . import GoogleOAuth, AppleOAuth, LinkedInOAuth, MicrosoftOAuth


class AuthTokenValidator:
    """
    Token validator for third-party providers
    """

    provider_class_map = {
        "GOOGLE": GoogleOAuth,
        "APPLE": AppleOAuth,
        "MICROSOFT": MicrosoftOAuth,
        "LINKEDIN": LinkedInOAuth,
    }

    @staticmethod
    def validate(provider: str, token: str) -> UserInfo:
        try:
            if not AuthProviders.is_valid_provider(provider):
                raise APIException(ERROR_MESSAGES["provider_not_supported"])

            auth_provider = AuthTokenValidator.provider_class_map[provider]
            user_info = auth_provider.validate(token)

            if user_info.get("type") != "success":
                raise APIException(ERROR_MESSAGES["signin_failed"])

            return user_info

        except ValueError as err:
            raise ValidationError({"message": str(err)})
        except (Exception, APIException) as err:
            raise ValidationError({"message": str(err)})
