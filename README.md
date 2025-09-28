# 🧠 Intelligent Career Guidance Platform

A web application that analyzes resumes using advanced NLP and machine learning to provide personalized **job role recommendations**, **skill gap analysis**, and **upskilling course suggestions**.

> 🔧 Built with **FastAPI** for backend, **spaCy** for NLP, and designed for modular scalability.

---

## 📌 Features Implemented (So Far)

| Feature                           | Status |
|----------------------------------|--------|
| Resume upload (PDF)              | ✅ Done |
| PDF text extraction              | ✅ Done |
| Structured resume parsing        | ✅ Done |
| Skills, education, experience extraction | ✅ Done |

---

## 📂 Project Structure

Intelligent-Career-Guidance/
│
├── app/
│ ├── api/
│ │ └── upload_resume.py # API route for uploading and parsing resumes
│ ├── services/
│ │ └── resume_parser.py # NLP logic for extracting structured info
│ ├── main.py # FastAPI application entry point
│
├── data/ # Sample test resumes (not pushed to GitHub)
├── requirements.txt # Python dependencies
├── .gitignore
└── README.md # Project documentation (you are here)

---

## 🚀 How to Run the Project Locally

### 1. Clone the repo

```bash
git clone https://github.com/im-sg/Intelligent-Career-Guidance-Platform.git
cd Intelligent-Career-Guidance-Platform
2. Create & activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate  # Windows

3. Install dependencies
pip install -r requirements.txt

4. Download the spaCy language model
python3 -m spacy download en_core_web_sm

5. Run the development server
uvicorn app.main:app --reload

6. Open in browser:

Go to: http://127.0.0.1:8000/docs
 to access Swagger UI.

🎯 API Endpoints
POST /upload-resume/

Upload a PDF resume and receive structured data in response.

Request:

Content-Type: multipart/form-data

Field: file (PDF only)

Response:

{
  "filename": "resume.pdf",
  "parsed_data": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "skills": ["Python", "SQL", "Machine Learning"],
    "education": ["b.tech in computer science"],
    "experience": ["at XYZ Corp", "ABC Technologies"]
  }
}

🧠 Tech Stack

Python 3.8+

FastAPI – API development

spaCy – NLP for entity extraction

pdfplumber – Resume PDF parsing

Uvicorn – ASGI server

🔮 Upcoming Features

✅ [In Progress] Job Role Recommendation based on skills

🛠 Skill Gap Analysis

📚 Course Recommendations (via Coursera/Udemy APIs)

🔎 Job Search Integration (LinkedIn, Indeed, etc.)

🎨 Frontend (React or Streamlit)

🔒 User profiles & Authentication

✅ Contribution Workflow

Create a branch:

git checkout -b feature/your-feature-name


Make your changes, test locally

Commit your changes:

git add .
git commit -m "Add your feature"


Push your branch:

git push -u origin feature/your-feature-name

🧾 License

MIT License — feel free to use and build upon this project.

🙌 Acknowledgements

Final Year Capstone Project

Built to help students and job seekers get personalized career guidance powered by AI and NLP
