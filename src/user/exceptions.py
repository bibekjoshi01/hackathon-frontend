from rest_framework.exceptions import APIException


class EmailNotSetError(ValueError):
    def __init__(self):
        super().__init__("The given email must be set.")


class IsStaffError(ValueError):
    def __init__(self):
        super().__init__("Superuser must have is_staff=True.")


class IsSuperuserError(ValueError):
    def __init__(self):
        super().__init__("Superuser must have is_superuser=True.")


class UserRoleNotFound(APIException):
    status_code = 400
    default_code = "user_role_not_found"

    def __init__(self, user_role):
        message = (
            f"UserRole '{user_role}' not found. Please contact the administrator.",
        )

        self.detail = {"error": message}
        self.user_role = user_role
