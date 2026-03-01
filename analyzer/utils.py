import PyPDF2
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# load spacy model
nlp = spacy.load("en_core_web_sm")

# skill database
SKILLS_DB = [
    "python", "django", "html", "css", "javascript",
    "rest api", "git", "github",
    "mysql", "sqlite", "sql",
    "bootstrap", "tailwind",
    "machine learning", "nlp", "pandas", "numpy"
]


# 🔹 Extract text from PDF and clean it
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + " "

    # Clean text
    text = text.replace("\n", " ")
    text = text.replace("  ", " ")
    text = text.lower()

    # normalize common variations
    text = text.replace("apis", "api")
    text = text.replace("restful api", "rest api")

    return text


# 🔹 Better similarity using TF-IDF
def calculate_similarity(resume_text, job_desc):
    # TF-IDF similarity
    tfidf = TfidfVectorizer().fit_transform([resume_text, job_desc])
    text_similarity = cosine_similarity(tfidf)[0][1]

    # Skill matching score
    resume_skills = extract_skills_spacy(resume_text)
    job_skills = extract_skills_spacy(job_desc)

    if len(job_skills) > 0:
        skill_match_ratio = len(set(resume_skills) & set(job_skills)) / len(job_skills)
    else:
        skill_match_ratio = 0

    # Combine both (weighted)
    final_score = (0.4 * text_similarity) + (0.6 * skill_match_ratio)

    return round(final_score * 100, 2)

# 🔹 Improved skill extraction using substring match
def extract_skills_spacy(text):
    text = text.lower()
    extracted_skills = set()

    for skill in SKILLS_DB:
        if skill in text:
            extracted_skills.add(skill)

    return list(extracted_skills)


# 🔹 Suggestions Generator
def generate_suggestions(missing_skills):
    suggestions = []

    for skill in missing_skills:
        if skill == "javascript":
            suggestions.append("Add JavaScript to improve frontend skills")
        elif skill == "rest api":
            suggestions.append("Mention REST API experience in your projects")
        elif skill == "git":
            suggestions.append("Add Git and GitHub project links")
        elif skill == "bootstrap":
            suggestions.append("Add Bootstrap for UI design skills")
        elif skill == "sql":
            suggestions.append("Include SQL database experience")
        elif skill == "django":
            suggestions.append("Add Django projects to your resume")
        elif skill == "python":
            suggestions.append("Highlight your Python programming experience")
        else:
            suggestions.append(f"Consider adding {skill} to your resume")

    return suggestions