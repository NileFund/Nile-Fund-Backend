from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        if isinstance(data, dict) and 'detail' in data and len(data) == 1:
            message = str(data['detail'])
            details = {}
        elif isinstance(data, dict):
            message = 'Validation failed.'
            details = data
        else:
            message = str(data)
            details = {}

        response.data = {
            'error':   True,
            'message': message,
            'details': details,
        }

    return response