from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


def validate_file_extension(value):
    file_extension_validator = FileExtensionValidator(
        allowed_extensions=["pdf", "doc", "docx", ".png", ".jpg"],
    )
    file_extension_validator(value)


def validate_file_size(value):
    # Define your desired maximum file size (in bytes)
    max_size = 5 * 1024 * 1024  # 5 MB

    if value.size > max_size:
        error_message = "File size exceeds the allowed limit (5 MB)."
        raise ValidationError(error_message)
