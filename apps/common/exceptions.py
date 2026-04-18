from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        data = response.data

        if isinstance(data, dict) and 'detail' in data and len(data) == 1:
            detail = data['detail']
            # Handle both string and list
            if isinstance(detail, list):
                message = str(detail[0])
            else:
                message = str(detail)
            details = {}
        elif isinstance(data, dict):
            message = 'Validation failed.'
            details = {
                k: [str(e) for e in v] if isinstance(v, list) else str(v)
                for k, v in data.items()
            }
        elif isinstance(data, list):
            message = str(data[0]) if data else 'Validation failed.'
            details = {}
        else:
            message = str(data)
            details = {}

        response.data = {
            'error': True,
            'message': message,
            'details': details,
        }
    return response