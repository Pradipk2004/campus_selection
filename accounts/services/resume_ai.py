import re

SKILL_DICT = {"python","django","rest","drf","javascript","react","sql","postgresql","docker","aws","git"}

def extract_skills_from_text(text: str):
    tokens = re.findall(r"[A-Za-z+#\.]+", text.lower())
    found = set()
    for t in tokens:
        if t in SKILL_DICT:
            found.add(t)
    return sorted(found)

def feedback_for_job_fit(student_skills: set, desired_skills: set):
    missing = sorted(desired_skills - student_skills)
    strengths = sorted(student_skills & desired_skills)
    lines = []
    if strengths:
        lines.append(f"Strengths: {', '.join(strengths)}.")
    if missing:
        lines.append(f"Suggested to learn: {', '.join(missing)}.")
    if not lines:
        lines.append("Good coverage. Keep projects ready to showcase.")
    return " ".join(lines)
