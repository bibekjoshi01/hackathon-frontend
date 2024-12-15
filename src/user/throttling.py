from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    rate = "3/minute"  # Specify the desired rate limit per hour
    def throttle_response(self, request, exception):
        message = "You have exceeded the maximum attempts."
        response = Response(message, status=429)
        response["Retry-After"] = 60
        return response
