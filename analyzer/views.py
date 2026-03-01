from django.shortcuts import render
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

        # extract text
        resume_text = extract_text_from_pdf(resume_file)

        # similarity score
        score = calculate_similarity(resume_text, job_desc)

        # skill extraction
        resume_skills = extract_skills_spacy(resume_text)
        job_skills = extract_skills_spacy(job_desc)

        matching_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))

        # suggestions
        suggestions = generate_suggestions(missing_skills)

        return render(request, 'result.html', {
            'name': name,
            'score': score,
            'matching_skills': matching_skills,
            'missing_skills': missing_skills,
            'suggestions': suggestions
        })

    return render(request, 'upload.html')