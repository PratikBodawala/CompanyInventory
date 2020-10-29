from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.

    if response is None:
        #     response.data['status_code'] = response.status_code
        # else:
        if isinstance(exc, ProtectedError):
            if isinstance(exc.args, (list, dict)):
                data = exc.args
            else:
                data = {'detail': ErrorDetail(exc.args[0], code='protected_error')}
            response = Response(data, status=status.HTTP_400_BAD_REQUEST)

    return response
