from django.shortcuts import render
from .models import RequestLog

def request_log_list(request):
    logs = RequestLog.objects.order_by('-timestamp')[:10]
    return render(request, 'audit/request_logs.html', {'logs': logs})
