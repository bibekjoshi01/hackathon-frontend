from rest_framework import serializers

from src.magazine.models import Magazine


# Magazine UUID field
class MagazineUUIDSerializerField(serializers.UUIDField):
    def to_internal_value(self, data):
        try:
            return Magazine.objects.get(uuid=data, is_active=True, is_archived=False)
        except Magazine.DoesNotExist as err:
            error_message = "Invalid magazine UUID"
            raise serializers.ValidationError(error_message) from err


class NotFoundSerializer404(serializers.Serializer):
    """404 Not Found Response"""

    message = serializers.CharField(max_length=255)


class ValidationErrorSerializer400(serializers.Serializer):
    """400 Validation Error Response"""

    error = serializers.CharField(max_length=255)


class SerializerValidationError400(serializers.Serializer):
    """Serializers Field Validation Error Response"""

    error = serializers.ListField(child=serializers.CharField())


class CreatedSuccessfullySerializer201(serializers.Serializer):
    """201 Serializers Created Successfully Response"""

    message = serializers.CharField(max_length=255)


class UnauthorizedSerializer401(serializers.Serializer):
    """401 Unauthorized Response"""

    detail = serializers.CharField(max_length=255)
