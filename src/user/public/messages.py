from django.utils.translation import gettext_lazy as _

ERROR_MESSAGES = {
    "account_disabled": _("Account Disabled."),
    "signin_failed": _("Unable to sign in. Please try again."),
    "provider_not_supported": _("This third-party provider is not supported."),
    "email_not_verified": _("Email verification failed."),
    "username_exists": _("This username is already taken."),
    "email_exists": _("An account with this email address already exists."),
    "phone_exists": _("A user with this phone number already exists."),
    "missing_roles": _("Please select at least one user group."),
}

LOGIN_SUCCESS = _("You have successfully logged in.")
LOGOUT_SUCCESS = _("You have successfully logged out.")
INVALID_CREDENTIALS = _("Invalid credentials. Please try again.")
PROFILE_UPDATED = _("Profile updated successfully.")

# flake8: noqa
INVALID_PASSWORD = _("Incorrect password. Please try again.")
ACCOUNT_DISABLED = _(
    "Your account has been disabled. Please contact support for assistance."
)
VERIFICATION_EMAIL_SENT = _(
    "A verification email has been sent to {email}. It is valid for 10 minutes."
)
ACCOUNT_VERIFIED = _("Your Account Verified Successfully.")
ACCOUNT_NOT_FOUND = _("Account with email {email} do not exists.")
PASSWORD_RESET_LINK_SENT = _(
    "A password rest link has been sent to {email}. It is valid for 10 minutes."
)
PASSWORD_CHANGED = _("Password changed successfully.")
OLD_PASSWORD_INCORRECT = _("Incorrect old password.")
PASSWORDS_NOT_MATCH = _("New password and confirm password do not match.")
SAME_OLD_NEW_PASSWORD = _("New password must be different from old password.")
LINK_EXPIRED = _("Link has expired. Please try again.")
INVALID_LINK = _("Invalid link. Please try again.")
ALREADY_VERIFIED = _("Account already verified. Please log in.")

UNKNOWN_ERROR = _("An Unknown error occured.")
