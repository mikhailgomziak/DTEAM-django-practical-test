from django.shortcuts import render, get_object_or_404
from .models import CV

def cv_list_view(request):
    cvs = CV.objects.prefetch_related('skills', 'projects', 'contacts').all()
    return render(request, 'main/cv_list.html', {'cvs': cvs})

def cv_detail_view(request, pk):
    cv = get_object_or_404(
        CV.objects.prefetch_related('skills', 'projects', 'contacts'),
        pk=pk
    )
    return render(request, 'main/cv_detail.html', {'cv': cv})

