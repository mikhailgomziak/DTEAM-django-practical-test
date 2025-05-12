from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from django.contrib import messages
import json

from .models import CV
from .serializers import CVSerializer

from weasyprint import HTML
from .tasks import send_cv_pdf_email
from .translate import translate_text

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

# views.py
@csrf_exempt
def translate_cv_view(request, cv_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body)
        target_language = data.get('language')

        if not target_language:
            return JsonResponse({'status': 'error', 'message': 'Missing target language'}, status=400)

        cv = get_object_or_404(CV, id=cv_id)

        fields_to_translate = {
            'First Name': cv.firstname,
            'Last Name': cv.lastname,
            'Bio': cv.bio,
        }

        skills_map = {f"{skill.id}": skill for skill in cv.skills.all()}
        for skill_id, skill in skills_map.items():
            fields_to_translate[f"Skill Name ({skill_id})"] = skill.name
            fields_to_translate[f"Skill Level ({skill_id})"] = skill.level

        projects_map = {f"{project.id}": project for project in cv.projects.all()}
        for project_id, project in projects_map.items():
            fields_to_translate[f"Project Title ({project_id})"] = project.title
            fields_to_translate[f"Project Description ({project_id})"] = project.description

        translations = translate_text(fields_to_translate, target_language)

        # Save CV translations
        cv.firstname_translated = translations.get("First Name", "")
        cv.lastname_translated = translations.get("Last Name", "")
        cv.bio_translated = translations.get("Bio", "")
        cv.save()

        # Save Skill translations
        for key, skill in skills_map.items():
            skill.name_translated = translations.get(f"Skill Name ({key})", "")
            skill.level_translated = translations.get(f"Skill Level ({key})", "")
            skill.save()

        # Save Project translations
        for key, project in projects_map.items():
            project.title_translated = translations.get(f"Project Title ({key})", "")
            project.description_translated = translations.get(f"Project Description ({key})", "")
            project.save()

        return JsonResponse({'status': 'success', 'message': 'Translated and stored in separate fields.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


class CVViewSet(viewsets.ModelViewSet):
    queryset = CV.objects.all()
    serializer_class = CVSerializer
