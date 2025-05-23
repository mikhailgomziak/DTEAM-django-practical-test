from django.conf import settings

def settings_context(request):
    databases = {}
    for alias, config in settings.DATABASES.items():
        databases[alias] = config.copy()
        # Convert NAME to string if it's a Path
        if hasattr(config.get('NAME'), '__fspath__'):
            databases[alias]['NAME'] = str(config['NAME'])
    
    return {
        'debug': settings.DEBUG,
        'project_name': getattr(settings, 'PROJECT_NAME', 'My Site'),
        'language_code': getattr(settings, 'LANGUAGE_CODE', 'en-use'),
        'time_zone': getattr(settings, 'TIME_ZONE', 'UTC'),
        'use_ssl': settings.EMAIL_USE_SSL,
        'use_tls': settings.EMAIL_USE_TLS,
        'email_backend': settings.EMAIL_BACKEND,
        'email_host': settings.EMAIL_HOST,
        'databases': databases
    }