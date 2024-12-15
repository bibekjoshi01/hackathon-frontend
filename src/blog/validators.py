from django.conf import settings
from django.core.exceptions import ValidationError


def validate_blog_media(image):
    file_size = image.size
    limit_byte_size = settings.BLOG_MEDIA_MAX_UPLOAD_SIZE
    if file_size > limit_byte_size:
        # converting into kb
        f = limit_byte_size / 1024
        # converting into MB
        f = f / 1024
        error_message = f"Max size of file is {f} MB"
        raise ValidationError(error_message)
