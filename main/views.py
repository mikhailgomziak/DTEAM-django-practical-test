from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from .models import CV
from .serializers import CVSerializer

from weasyprint import HTML

def cv_list_view(request):
    cvs = CV.objects.prefetch_related('skills', 'projects', 'contacts').all()
    return render(request, 'main/cv_list.html', {'cvs': cvs})

def cv_detail_view(request, pk):
    cv = get_object_or_404(
        CV.objects.prefetch_related('skills', 'projects', 'contacts'),
        pk=pk
    )
    return render(request, 'main/cv_detail.html', {'cv': cv})

def download_cv_pdf(request, pk):
    cv = get_object_or_404(CV.objects.prefetch_related('skills', 'projects', 'contacts'), pk=pk)
    template = get_template("main/cv_pdf.html")
    html = template.render({"cv": cv})

    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{cv.firstname}_{cv.lastname}_CV.pdf"'
    return response

class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
