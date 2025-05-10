import threading
from django.utils.timezone import now
from .models import RequestLog

# Used threading to prevent blocking
request_log_lock = threading.Lock()

class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Avoiding logging for static/admin endpoints
        if request.path.startswith('/static/') or request.path.startswith('/admin/'):
            return response

        def log_request():
            RequestLog.objects.create(
                timestamp=now(),
                method=request.method,
                path=request.path,
                query_string=request.META.get('QUERY_STRING', ''),
                remote_ip=self.get_client_ip(request),
                user=request.user if request.user.is_authenticated else None
            )

        # Lock for thread safety
        with request_log_lock:
            log_request()

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')
