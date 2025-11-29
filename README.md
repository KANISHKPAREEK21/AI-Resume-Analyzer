# 📘 **AI Resume Analyzer**

**AI Resume Analyzer backend using FastAPI, SQLite, MongoDB, and Azure OpenAI Chat Completion.**
A modern, AI-powered backend service that analyzes resumes, extracts technical and soft skills, identifies strengths and gaps, and generates actionable improvement suggestions using Azure OpenAI’s Chat Completion models.

This project demonstrates clean architecture, secure authentication, hybrid data storage (SQL + NoSQL), and a production-ready API design — all written in **Python 3.14**.

---

## 🚀 **Features Overview**

### 🔹 **Resume Analysis using Azure OpenAI**

* Summarizes professional experience
* Extracts technical & soft skills
* Identifies strengths and weaknesses
* Suggests improvements for target roles
* Stores raw LLM responses to MongoDB

### 🔹 **User Authentication**

* JWT-based secure auth
* Password hashing with Argon2 (Passlib)
* Fully protected routes

### 🔹 **Hybrid Storage Architecture**

* **SQLite** (users, resumes, structured analysis)
* **MongoDB** (raw resume text + AI logs)

### 🔹 **Clean FastAPI Backend**

* Organized module structure
* Dependency injection
* Automatic interactive API docs (Swagger UI)

---

# 🧰 **Tech Stack**

### **Language & Runtime**

* **Python 3.14** ← *highlighting the use of the latest Python version*

### **Backend**

* FastAPI — high-performance web framework
* SQLAlchemy 2.x — ORM with session management
* Pydantic 2.x + pydantic-settings — validation & configuration
* Uvicorn — ASGI server

### **AI**

* Azure OpenAI Service — Chat Completion API for resume analysis
* httpx — async client for calling Azure APIs

### **Databases**

* SQLite — primary structured database
* MongoDB — secondary store for raw logs (via PyMongo)

### **Security & Auth**

* python-jose — JWT tokens
* Passlib (argon2) — password hashing

---

# 🗂️ **Project Structure**

```
ai-resume-analyzer/
├─ app/
│  ├─ init.py
│  ├─ main.py                     # FastAPI app entry point
│  ├─ core/
│  │  ├─ __init__.py
│  │  ├─ config.py                # Settings & environment config
│  │  ├─ database.py              # SQLite session & engine
│  │  ├─ mongo.py                 # MongoDB connection
│  │  └─ security.py              # Auth, hashing, token utils
│  ├─ models/                     # SQLAlchemy ORM models
│  │  ├─ __init__.py
│  │  ├─ user.py
│  │  ├─ resume.py
│  │  └─ analysis.py
│  ├─ schemas/                    # Pydantic schemas
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  ├─ user.py
│  │  ├─ resume.py
│  │  └─ analysis.py
│  ├─ routes/                     # API route definitions
│  │  ├─ __init__.py
│  │  ├─ auth.py
│  │  └─ resumes.py
│  └─ services/
│     ├─ __init__.py
│     └─ ai_client.py             # Azure OpenAI analysis logic
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

# 🧱 **High-Level Architecture Diagram**

```
                   ┌─────────────────────────────┐
                   │         FastAPI API         │
                   │     (app/main.py + routes)  │
                   └──────────────┬──────────────┘
                                  │
                         Auth (JWT, Security)
                                  │
         ┌────────────────────────┼────────────────────────┐
         │                        │                        │
         ▼                        ▼                        ▼
┌────────────────┐     ┌────────────────────┐     ┌─────────────────────┐
│   SQLite DB    │     │   Azure OpenAI     │     │      MongoDB        │
│ users, resumes │     │ analyze resume     │     │ raw resumes + logs  │
│ analyses       │     │ via chat completions│    │ unstructured data   │
└────────────────┘     └────────────────────┘     └─────────────────────┘
```

---

# 🔁 **API Flow (High-Level Illustration)**

```
Client
  │
  ├─▶ Login (POST /auth/login)
  │       ▼
  │     JWT Issued
  │
  ├─▶ Upload Resume (POST /resumes/)
  │       ▼
  │   Stored to SQLite + MongoDB
  │
  ├─▶ Analyze Resume (POST /resumes/{id}/analyze)
  │       ▼
  │   Azure OpenAI → structured insights
  │       ▼
  │   Save to SQLite (analysis table)
  │   Save raw logs to MongoDB
  │
  └─▶ Fetch Results (GET /resumes/{id}/analysis)
          ▼
       JSON output
```

---

# ⚙️ **Installation & Setup**

## 1️⃣ Clone the repository

```bash
git clone https://github.com/KANISHKPAREEK21/AI-Resume-Analyzer.git
cd AI-Resume-Analyzer
```

## 2️⃣ Create a virtual environment

```bash
python3.14 -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Configure environment variables

Copy the example file:

```bash
cp .env.example .env
```

Fill in:

```
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_DEPLOYMENT=
AZURE_OPENAI_API_VERSION=
JWT_SECRET_KEY=
MONGO_URI=
```

## 5️⃣ Run the server

```bash
uvicorn app.main:app --reload
```

API docs available at:

```
http://127.0.0.1:8000/docs
```

---

# 🔒 **Authentication Overview**

* Users register with email/password
* Passwords are hashed using **argon2**
* Users authenticate with `/auth/login`
* Access token (JWT) is required for all resume routes
* Tokens must be included as:

```
Authorization: Bearer <token>
```

---

# 🧪 **Testing the API (Example)**

### Create a resume

```bash
curl -X POST http://127.0.0.1:8000/resumes/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
        "title": "Software Engineer Resume",
        "resume_text": "Your resume...",
        "target_role": "Backend Developer",
        "job_description": "Role description here"
      }'
```

---

# 🤝 **Contributing**

Contributions are welcome — whether it's improving the analysis logic, enhancing security, or adding support for new LLM providers.

---

# 📜 **License**

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute this project with proper attribution.

---

# 🎉 **Final Notes**

This backend is designed with clean architecture principles, production-ready API structure, and modern Python standards. This project demonstrates:

* AI-driven backend engineering skills
* AI integration expertise
* Experience with SQL + NoSQL hybrid data systems
* Authentication, security, and structured API design
* Clean, scalable FastAPI design
