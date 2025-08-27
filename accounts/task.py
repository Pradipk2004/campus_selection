from celery import shared_task
from .models import StudentProfile, ResumeAnalysis
from .services.resume_ai import extract_skills_from_text, feedback_for_job_fit

def pdf_to_text(file_path:str) -> str:
    # minimal placeholder; integrate pdfminer later
    try:
        from pdfminer.high_level import extract_text
        return extract_text(file_path) or ""
    except Exception:
        return ""

@shared_task
def analyze_resume_for_user(user_id):
    sp = StudentProfile.objects.select_related("user").get(user_id=user_id)
    if not sp.resume:
        return
    text = pdf_to_text(sp.resume.path)
    detected = extract_skills_from_text(text)
    ra, _ = ResumeAnalysis.objects.get_or_create(student=sp.user)
    ra.skills_detected = detected
    # generic feedback (job-agnostic); you can also compute per-job fits elsewhere
    ra.summary = f"Detected skills: {', '.join(detected)}." if detected else "No common skills detected."
    ra.save()
