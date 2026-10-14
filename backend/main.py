from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_connection
from analyzer import analyze_resume 

app = FastAPI(title="JobNex API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    resume: Optional[str] = None
    job_description: Optional[str] = None
    resume_text: Optional[str] = None
    jd_text: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "resume": "Python developer with Python, SQL and React skills.",
                "job_description": "Looking for a Python developer with SQL and FastAPI."
            }
        }


@app.get("/")
def home():
    return {
        "message": "Resume Analyzer Backend is Running"
    }


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    # Support both 'resume'/'job_description' and 'resume_text'/'jd_text'
    resume_text = request.resume or request.resume_text
    jd_text = request.job_description or request.jd_text

    if not resume_text or not jd_text:
        raise HTTPException(
            status_code=400,
            detail="Please provide both resume and job description text."
        )

    # 1. Run the analysis
    result = analyze_resume(resume_text, jd_text)
    matched_skills = ", ".join(result["matched_skills"])
    missing_skills = ", ".join(result["missing_skills"])
    suggestions = " | ".join(result["suggestions"])
    match_score = result["match_score"]

    # 2. Save into MySQL Database
    connection = None
    cursor = None
    analysis_id = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO resume_analyzer (resume_text, Jd_text, matched_skills, missing_skills, matched_score, suggestions)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (resume_text, jd_text, matched_skills, missing_skills, match_score, suggestions)
        )

        connection.commit()
        analysis_id = cursor.lastrowid

    except Exception as error:
        if connection is not None and connection.is_connected():
            connection.rollback()
        # Return analysis even if database connection fails, with error details
        return {
            "status": "partial_success",
            "message": f"Analysis completed, but DB save failed: {str(error)}",
            "score": match_score,
            "matched_skills": result["matched_skills"],
            "missing_skills": result["missing_skills"],
            "suggestions": result["suggestions"]
        }

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

    return {
        "message": "Analysis request saved successfully",
        "Analysis_id": analysis_id,
        "score": match_score,
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "suggestions": result["suggestions"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)