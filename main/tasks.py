from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO

@shared_task
def send_cv_pdf_email(cv_id, email):
    from .models import CV
    cv = CV.objects.get(pk=cv_id)
    
    from django.conf import settings
    print(settings.EMAIL_HOST_PASSWORD)
    html_string = render_to_string("main/cv_detail.html", {"cv": cv})

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)
    
    message = EmailMessage(
        subject=f"Your CV: {cv.firstname} {cv.lastname}",
        body="Attached is the PDF version of the CV.",
        to=[email]
    )
    message.attach(f"cv_{cv.id}.pdf", pdf_file.read(), "application/pdf")

    message.send()
    
    return f"PDF sent to {email}"

