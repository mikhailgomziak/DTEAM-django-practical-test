from django.shortcuts import render

def settings_view(request):
    return render(request, 'core/settings_page.html')
