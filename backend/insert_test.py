"""
insert_test.py
Script to test inserting and retrieving resume & analysis data from MySQL.
"""

import sys
import database

def run_insert_test():
    print("=" * 60)
    print("       JobNex - MySQL Insert & Query Test")
    print("=" * 60)

    # Step 1: Ensure database and tables exist
    print("[1/3] Initializing DB schema...")
    if not database.init_db():
        print("      FAILED: Could not connect or initialize database.")
        print("      Please ensure MySQL is running and .env has the right credentials.")
        return False
    print("      SUCCESS: DB schema ready.")

    # Step 2: Insert a sample Resume
    print("\n[2/3] Inserting sample Resume into 'resumes' table...")
    sample_name = "Alex Johnson"
    sample_email = "alex.johnson@example.com"
    sample_phone = "+1-555-0199"
    sample_skills = ["Python", "FastAPI", "SQL", "Docker", "React"]
    sample_exp = "3 years as Full Stack Developer building REST APIs and microservices."
    sample_edu = "B.S. in Computer Science"
    sample_summary = "Enthusiastic developer with expertise in Python backends and modern web applications."
    sample_raw = f"{sample_name} | {sample_email} | Skills: {', '.join(sample_skills)}"

    try:
        resume_id = database.save_resume(
            name=sample_name,
            email=sample_email,
            phone=sample_phone,
            skills=sample_skills,
            experience=sample_exp,
            education=sample_edu,
            summary=sample_summary,
            raw_text=sample_raw
        )
        print(f"      SUCCESS: Created Resume with ID = {resume_id}")
        
        # Verify by reading it back
        fetched_resume = database.get_resume_by_id(resume_id)
        print("      Fetched from DB:")
        print(f"       - ID:         {fetched_resume.get('id')}")
        print(f"       - Name:       {fetched_resume.get('name')}")
        print(f"       - Email:      {fetched_resume.get('email')}")
        print(f"       - Skills:     {fetched_resume.get('skills')}")
        print(f"       - Created At: {fetched_resume.get('created_at')}")
    except Exception as e:
        print(f"      FAILED to insert/fetch resume: {e}")
        return False

    # Step 3: Insert a sample Analysis into resume_analyzer table
    print("\n[3/3] Inserting sample Analysis into 'resume_analyzer' table...")
    sample_resume_text = "Proficient in Python, SQL, Docker, and REST APIs."
    sample_jd_text = "Looking for a backend engineer skilled in Python, SQL, React, FastAPI, and Docker."
    sample_score = 80.0
    matched = ["python", "sql", "docker"]
    missing = ["react", "fastapi"]
    suggestions = [
        "Add or highlight 'react' in your resume for this position.",
        "Add or highlight 'fastapi' in your resume for this position."
    ]

    try:
        analysis_id = database.save_analysis(
            resume_text=sample_resume_text,
            jd_text=sample_jd_text,
            matched_score=sample_score,
            matched_skills=matched,
            missing_skills=missing,
            suggestions=suggestions
        )
        print(f"      SUCCESS: Created Analysis Record with Analysis_Id = {analysis_id}")

        # Verify by reading it back
        fetched_analysis = database.get_analysis_by_id(analysis_id)
        print("      Fetched from DB:")
        print(f"       - Analysis_Id:    {fetched_analysis.get('Analysis_Id')}")
        print(f"       - Matched Score:  {fetched_analysis.get('matched_score')}%")
        print(f"       - Matched Skills: {fetched_analysis.get('matched_skills')}")
        print(f"       - Missing Skills: {fetched_analysis.get('missing_skills')}")
        print(f"       - Suggestions:    {fetched_analysis.get('suggestions')}")
        print(f"       - Created At:     {fetched_analysis.get('created_At')}")
    except Exception as e:
        print(f"      FAILED to insert/fetch analysis: {e}")
        return False

    print("\n" + "=" * 60)
    print(" ALL TESTS PASSED SUCCESSFULLY!")
    print(" You can now view these records in MySQL Workbench:")
    print(f"   SELECT * FROM `{database.DB_NAME}`.`resumes`;")
    print(f"   SELECT * FROM `{database.DB_NAME}`.`resume_analyzer`;")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = run_insert_test()
    sys.exit(0 if success else 1)
