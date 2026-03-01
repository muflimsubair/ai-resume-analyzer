from django.shortcuts import render
from .models import ResumeAnalysis
from .utils import (
    extract_text_from_pdf,
    calculate_similarity,
    extract_skills_spacy,
    generate_suggestions
)

# Home page
def home(request):
    return render(request, 'home.html')

# About page
def about(request):
    return render(request, 'about.html')

# Upload + Analyze
def upload_resume(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        job_desc = request.POST.get('job_description')
        resume_file = request.FILES.get('resume')

        # 1️⃣ Extract text
        resume_text = extract_text_from_pdf(resume_file)

        # 2️⃣ Calculate score FIRST
        score = calculate_similarity(resume_text, job_desc)

        # 3️⃣ Extract skills
        resume_skills = extract_skills_spacy(resume_text)
        job_skills = extract_skills_spacy(job_desc)

        matching_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))

        # 4️⃣ Generate suggestions
        suggestions = generate_suggestions(missing_skills)

        # 5️⃣ SAVE to database (after score is created)
        ResumeAnalysis.objects.create(
            name=name,
            score=score
        )

        # 6️⃣ Return result
        return render(request, 'result.html', {
            'name': name,
            'score': score,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'suggestions': suggestions
        })

    return render(request, 'upload.html')

def dashboard(request):
    data = ResumeAnalysis.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'data': data})