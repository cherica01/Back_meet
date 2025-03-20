# api/utils.py
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF that adds more details to the response.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # If response is None, there was an unhandled exception
    if response is None:
        logger.error(f"Unhandled exception: {exc}")
        return Response(
            {
                'detail': 'An unexpected error occurred.',
                'type': str(type(exc).__name__),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Add more context to the response
    if hasattr(exc, 'default_code'):
        response.data['code'] = exc.default_code
    
    # Add request info for debugging
    if 'request' in context:
        request = context['request']
        response.data['request_id'] = request.META.get('HTTP_X_REQUEST_ID', '')
    
    return response


def get_client_ip(request):
    """
    Get client IP address from request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_api_request(request, response=None, error=None):
    """
    Log API request details for monitoring and debugging.
    """
    data = {
        'method': request.method,
        'path': request.path,
        'user_id': getattr(request.user, 'id', None),
        'ip': get_client_ip(request),
        'user_agent': request.META.get('HTTP_USER_AGENT', ''),
    }
    
    if response:
        data['status_code'] = response.status_code
    
    if error:
        data['error'] = str(error)
    
    logger.info(f"API Request: {data}")