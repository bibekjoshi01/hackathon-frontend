from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError


def validate_positive_integer(value):
    if value <= 0:
        error_message = _("Value must be a positive integer")
        raise ValidationError(error_message)


def validate_alpha(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        error_message = _('"%(value)s" contains non-alphabetic characters') % {
            "value": value,
        }
        raise ValidationError(error_message)
