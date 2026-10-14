"""
analyzer.py
Resume and Job Description analysis module for JobNex.
Analyzes skill match, calculates match scores, and provides actionable suggestions.
"""

import re


def is_skill_present(skill: str, text: str) -> bool:
    """
    Check if a skill is present in text using case-insensitive, word-aware matching.
    Handles compound skills (e.g., 'HTML/CSS') and symbol-heavy names (e.g., 'C++').
    """
    if not skill or not text:
        return False

    cleaned_skill = skill.strip().lower()
    lower_text = text.lower()

    # Handle compound skills like "HTML/CSS"
    if "/" in cleaned_skill:
        parts = [p.strip() for p in cleaned_skill.split("/") if p.strip()]
        if cleaned_skill in lower_text or all(is_skill_present(p, lower_text) for p in parts):
            return True

    # Word boundary / symbol-aware regex
    escaped = re.escape(cleaned_skill)
    pattern = rf"(?<![a-zA-Z0-9_]){escaped}(?![a-zA-Z0-9_])"
    return bool(re.search(pattern, lower_text))


def analyze_resume(resume: str, jd: str, skills: list = None) -> dict:
    """
    Analyzes resume text against a job description text to compute matched skills,
    missing/unmatched skills, match score, and recommendations.

    Args:
        resume (str): Candidate's resume text.
        jd (str): Target job description text.
        skills (list, optional): Benchmark skill list. Defaults to ["Python", "Java", "SQL", "C++", "HTML/CSS"].

    Returns:
        dict: {
            "match_score": float,
            "score": float,
            "matched_skills": list[str],
            "unmatched_skills": list[str],
            "missing_skills": list[str],
            "suggestions": list[str],
            "total_skills_evaluated": int
        }
    """
    if skills is None:
        skills = ["Python", "Java", "SQL", "C++", "HTML/CSS"]

    resume_text = (resume or "").lower()
    jd_text = (jd or "").lower()

    matched_skills = []
    unmatched_skills = []
    missing_skills = []
    suggestions = []

    # Detect skills mentioned in Job Description
    jd_required_skills = [s for s in skills if is_skill_present(s, jd_text)]

    # If JD specifies target skills, evaluate against those; otherwise against all benchmark skills
    target_skills = jd_required_skills if jd_required_skills else skills

    for skill in skills:
        in_resume = is_skill_present(skill, resume_text)
        in_jd = is_skill_present(skill, jd_text)

        if in_resume and in_jd:
            matched_skills.append(skill)
        else:
            unmatched_skills.append(skill)
            # If the skill was requested in JD but missing in resume
            if in_jd and not in_resume:
                missing_skills.append(skill)
                suggestions.append(f"Add '{skill}' to your resume to match the job requirements.")

    # If JD didn't mention specific skills, missing skills are any target skills not in resume
    if not jd_required_skills:
        missing_skills = [s for s in unmatched_skills if not is_skill_present(s, resume_text)]
        for s in missing_skills:
            suggestions.append(f"Consider adding '{s}' to your resume if you have experience with it.")

    # Calculate match percentage
    denominator = len(target_skills) if target_skills else len(skills)
    if denominator > 0:
        match_score = round((len(matched_skills) / denominator) * 100, 2)
    else:
        match_score = 0.0

    return {
        "match_score": match_score,
        "score": match_score,
        "matched_skills": matched_skills,
        "unmatched_skills": unmatched_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions,
        "total_skills_evaluated": len(target_skills),
    }
