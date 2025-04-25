from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import exception_handler

def custom_authentication_failed_handler(exc, context):
    # Check if it's an authentication error
    if isinstance(exc, AuthenticationFailed):
        return Response(
            {
                "success": False,
                "message": "Authentication credentials were not provided."
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    # Call the default exception handler for other errors
    return exception_handler(exc, context)