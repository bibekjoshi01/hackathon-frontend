from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle


class LoginThrottle(UserRateThrottle):
    rate = "20/minute"  

    def throttle_response(self, request, exception):
        message = "You have exceeded the maximum attempts."
        response = Response(message, status=429)
        response["Retry-After"] = 60
        return response
