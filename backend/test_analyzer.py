from analyzer import analyze_resume
import database

resume_text = "Python developer with Python, SQL and React skills."
jd_text = "Looking for a Python developer with SQL and FastAPI."

# 1. Perform Resume Analysis
result = analyze_resume(resume_text, jd_text)
print("Analysis Result:")
print(result)

# 2. Save into MySQL Workbench database ('jobnex', table 'resume_analyzer')
try:
    analysis_id = database.save_analysis(
        resume_text=resume_text,
        jd_text=jd_text,
        matched_score=result["score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
        suggestions=result["suggestions"]
    )
    print("\n[SUCCESS] Saved to MySQL Workbench table 'resume_analyzer' with Analysis_Id = " + str(analysis_id))
    print("Run `SELECT * FROM resume_analyzer;` in MySQL Workbench to view the new record!")
except Exception as e:
    print("\n[FAILED] Could not connect or save to MySQL Workbench: " + str(e))
    print("-> Please check that DB_PASSWORD in backend/.env matches your MySQL Workbench password.")