# JobNex — Next-Gen Resume & Job Matching Intelligence
### *An Algonex Product*

![JobNex Product Release](https://img.shields.io/badge/Release-v1.0.0-blue?style=for-the-badge&logo=rocket)
![Algonex](https://img.shields.io/badge/Product%20By-Algonex-4F46E5?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/Database-MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Python](https://img.shields.io/badge/Language-Python%203.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 🚀 About JobNex

**JobNex** is an intelligent, automated talent intelligence and resume-job matching platform built by **Algonex**. Designed as a turnkey enterprise and candidate matching product, JobNex bridges the gap between job seekers and hiring teams by analyzing resumes against target job descriptions with precision, calculating weighted compatibility scores, identifying skill deficits, and delivering immediate, actionable career suggestions.

> **Note:** JobNex is not merely a project — it is a production-oriented product developed under the **Algonex** product suite.

---

## ✨ Core Product Capabilities

- **🎯 Context-Aware Match Scoring**: Evaluates candidate resumes against target job specifications with symbol-aware tokenization and compound skill parsing (e.g., `HTML/CSS`, `C++`).
- **🔍 Skill Gap Analysis**: Detects exactly which core skills are matched and pinpoints missing competencies required by the employer.
- **💡 Actionable Recommendations**: Generates tailored suggestions to guide candidates on enhancing their resumes for specific job requisitions.
- **🗄️ Enterprise Data Persistence**: Integrated MySQL storage supporting candidate profile indexing (`resumes`) and audit trails of matching outcomes (`resume_analyzer`).
- **⚡ High-Performance REST API**: Built on **FastAPI** for ultra-low latency inference, asynchronous operations, and auto-generated Swagger documentation.
- **💻 Dual Frontend Interfaces**:
  - Full-featured Management Dashboard (`backend/index.html`): candidate entry, real-time matching metrics, and live database queries.
  - Minimalist Client UI (`frontend/index.html`): distraction-free resume evaluator.

---

## 🏛️ System Architecture

```text
                       ┌───────────────────────────────┐
                       │    JobNex Client Interface    │
                       │   (Web Dashboard / Portal)    │
                       └──────────────┬────────────────┘
                                      │  HTTP / JSON
                                      ▼
                       ┌───────────────────────────────┐
                       │       FastAPI Gateway         │
                       │      (backend/main.py)        │
                       └──────┬─────────────────┬──────┘
                              │                 │
                   Evaluate   ▼                 ▼   Persist
             ┌─────────────────────────┐  ┌─────────────────────────┐
             │    Analyzer Engine      │  │    Database Connector   │
             │  (backend/analyzer.py)  │  │   (backend/database.py) │
             └─────────────────────────┘  └────────────┬────────────┘
                                                       │
                                                       ▼
                                          ┌─────────────────────────┐
                                          │      MySQL Storage      │
                                          │  - resumes              │
                                          │  - resume_analyzer      │
                                          └─────────────────────────┘
```

---

## 📁 Repository Structure

```
JobNex/
├── backend/
│   ├── analyzer.py          # Core NLP & skill evaluation engine
│   ├── database.py          # MySQL database connection & CRUD handlers
│   ├── main.py              # FastAPI application server & routes
│   ├── index.html           # Full featured product dashboard UI
│   ├── script.js            # Dashboard interactive application logic
│   ├── style.css            # Dashboard styling system
│   ├── test_analyzer.py     # Skill matcher test & analysis script
│   ├── test_db.py           # Database connectivity diagnostic suite
│   ├── insert_test.py       # DB schema & data insertion verification
│   └── .env.example         # Sample backend environment configuration
├── frontend/
│   ├── index.html           # Standalone client matching interface
│   ├── script.js            # Client-side API request handler
│   └── style.css            # Client interface styling
├── .env.example             # Project-wide sample environment configuration
├── .gitignore               # Ignored runtime artifacts & environment keys
├── requirements.txt         # Production and development dependencies
└── README.md                # Product documentation
```

---

## 🛠️ Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **MySQL Server 8.0+** (or MySQL Workbench / cloud MySQL instance)

### 2. Installation

Clone the repository and set up your Python environment:

```bash
git clone https://github.com/anshulrevuru/jobnex_an_algonex_product.git
cd jobnex_an_algonex_product

# Optional: Create and activate virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env` in the root and/or `backend/` directory:

```bash
cp .env.example backend/.env
```

Edit `backend/.env` with your database credentials:
```ini
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=jobnex_db
```

### 4. Database Setup & Diagnostic Verification

Run the built-in diagnostic test to verify MySQL connectivity and auto-create database tables:

```bash
python backend/test_db.py
```

Run insertion verification to test end-to-end data persistence:

```bash
python backend/insert_test.py
```

### 5. Launch the JobNex API Server

```bash
cd backend
python main.py
```
Or with `uvicorn`:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

The API will be available at `http://127.0.0.1:8000`.
- **Interactive API Docs (Swagger UI)**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

### 6. Access the User Interface

- Open `frontend/index.html` or `backend/index.html` in any modern web browser to interact with the JobNex matching engine.

---

## 🔌 API Reference

### Health Check
```http
GET /
```
**Response:**
```json
{
  "message": "Resume Analyzer Backend is Running"
}
```

### Analyze Resume
```http
POST /api/analyze
Content-Type: application/json
```

**Request Body:**
```json
{
  "resume": "Software engineer proficient in Python, SQL, Docker, and REST APIs.",
  "job_description": "Looking for backend developer with Python, SQL, FastAPI, and Kubernetes."
}
```

**Response:**
```json
{
  "message": "Analysis request saved successfully",
  "Analysis_id": 1,
  "score": 66.67,
  "matched_skills": [
    "Python",
    "SQL"
  ],
  "missing_skills": [
    "FastAPI",
    "Kubernetes"
  ],
  "suggestions": [
    "Add 'FastAPI' to your resume to match the job requirements.",
    "Add 'Kubernetes' to your resume to match the job requirements."
  ]
}
```

---

## 🗄️ Database Schema

### Table: `resumes`
Stores candidate profile records.
| Column | Type | Description |
|---|---|---|
| `id` | INT AUTO_INCREMENT | Unique identifier (Primary Key) |
| `name` | VARCHAR(255) | Candidate's name |
| `email` | VARCHAR(255) | Contact email |
| `phone` | VARCHAR(50) | Contact phone number |
| `skills` | TEXT | Comma-separated list of identified skills |
| `experience`| TEXT | Professional background summary |
| `education` | TEXT | Academic qualifications |
| `summary` | TEXT | Executive profile summary |
| `raw_text` | LONGTEXT | Full unparsed resume text |
| `created_at`| TIMESTAMP | Submission timestamp |

### Table: `resume_analyzer`
Stores matching session outputs and audit logs.
| Column | Type | Description |
|---|---|---|
| `Analysis_Id` | INT AUTO_INCREMENT | Unique analysis session ID (Primary Key) |
| `resume_text` | LONGTEXT | Submitted resume input |
| `Jd_text` | LONGTEXT | Target job description input |
| `matched_score` | DECIMAL(5,2) | Percentage compatibility score |
| `matched_skills`| TEXT | Comma-delimited matching skills |
| `missing_skills`| TEXT | Skills requested by JD but missing |
| `suggestions` | TEXT | Tailored recommendation bullet points |
| `created_At` | TIMESTAMP | Execution timestamp |

---

## 🗺️ Product Roadmap

- [x] **v1.0.0**: Core skill matcher, FastAPI REST service, MySQL database layer, dual web dashboards.
- [ ] **v1.1.0**: PDF/DOCX resume file parsing and OCR ingestion.
- [ ] **v1.2.0**: Advanced LLM semantic evaluation for domain nuance & soft skills.
- [ ] **v2.0.0**: Multi-tenant recruiter portal with applicant ranking and candidate matching pipelines.

---

## 💼 Algonex

**JobNex** is engineered and maintained as an **Algonex** product.

- **Organization**: Algonex
- **Product**: JobNex (v1.0.0)
- **Repository**: [jobnex_an_algonex_product](https://github.com/anshulrevuru/jobnex_an_algonex_product)
