# Intelligent Career Guidance Platform 🎓

AI-powered web app that:
- Parses resumes (PDF)
- Extracts skills, experience, education
- Recommends job roles
- (Future) Suggests courses based on skill gaps

## 🧱 Tech Stack

- Backend: FastAPI (Python)
- NLP: spaCy, sentence-transformers
- PDF: pdfplumber
- Frontend: (Planned) React or Streamlit

## 🚀 How to Run

```bash
source venv/bin/activate
uvicorn app.main:app --reload
