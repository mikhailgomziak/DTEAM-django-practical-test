from django.http import HttpResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from django.contrib import messages

from .models import CV
from .serializers import CVSerializer

from weasyprint import HTML
from .tasks import send_cv_pdf_email

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

def send_cv_pdf_view(request, pk):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            send_cv_pdf_email.delay(cv_id=pk, email=email)
            messages.success(request, f"The CV PDF is being sent to {email}.")
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect("cv_detail", pk=pk)

class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
