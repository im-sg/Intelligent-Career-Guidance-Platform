# Intelligent Career Guidance Platform

An AI-powered career guidance platform that analyzes resumes and provides personalized job role recommendations with skill gap analysis and course suggestions.

## Features

- **Resume Analysis**: Upload and parse resumes to extract skills, experience, and education
- **ML-Powered Role Recommendations**: Get top matching job roles based on your profile
- **Interactive Skill Gap Analysis**: Visualize your strengths and identify skills to improve
- **Course Recommendations**: Get relevant course suggestions from Udemy and Coursera
- **Interactive Dashboard**: View detailed skill breakdowns with radar charts and progress bars
- **User Authentication**: Secure registration and login system with JWT tokens

## Tech Stack

### Backend
- **Language:** Python 3.8+
- **Web Framework:** FastAPI 0.115.5
- **NLP:** spaCy 3.7.2 (en_core_web_sm model)
- **ML:** scikit-learn 1.5.2 (Random Forest Classifier)
- **Database:** SQLite with SQLAlchemy ORM
- **File Processing:** PyPDF2, python-docx
- **Authentication:** JWT (JSON Web Tokens)

### Frontend
- **Framework:** React 18
- **Build Tool:** Vite
- **Visualization:** Recharts for radar charts and progress bars
- **HTTP Client:** Axios
- **Icons:** Lucide React
- **Routing:** React Router

### Dataset
- **Source:** Hugging Face (datasetmaster/resumes)
- **Size:** 2,500+ cleaned and categorized resumes
- **Format:** JSONL (JSON Lines)

## Project Structure

```
intelligent-career-platform/
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI application entry point
│   │   ├── routers/                     # API endpoints
│   │   │   ├── auth.py                  # Authentication (register, login)
│   │   │   ├── resume.py                # Resume upload and processing
│   │   │   └── roles.py                 # Job role recommendations
│   │   ├── services/                    # Business logic
│   │   │   ├── file_processor.py        # PDF/DOCX/TXT text extraction
│   │   │   ├── resume_parser.py         # spaCy NLP parsing
│   │   │   └── ml_role_analyzer.py      # Random Forest inference
│   │   ├── models/                      # Database models
│   │   │   ├── database.py              # SQLAlchemy models
│   │   │   └── schemas.py               # Pydantic validation schemas
│   │   ├── ml_models/                   # ML training pipeline
│   │   │   ├── data_generator.py        # Generate training data
│   │   │   ├── train_model.py           # Train Random Forest
│   │   │   └── saved_models/            # Trained model artifacts
│   │   └── utils/
│   │       └── auth.py                  # JWT utilities
│   ├── data/
│   │   ├── raw/
│   │   │   └── master_resumes.jsonl     # Downloaded dataset
│   │   ├── collected_resumes/           # Organized by job role
│   │   │   ├── ai_engineer/
│   │   │   ├── machine_learning_engineer/
│   │   │   ├── data_scientist/
│   │   │   └── ... (10 role folders)
│   │   ├── skills/
│   │   │   └── skills_taxonomy.json     # 52-skill taxonomy
│   │   ├── resume_metadata.csv          # Cleaned resume tracking
│   │   └── processed_resumes.json       # NLP-processed data
│   ├── scripts/
│   │   ├── download_dataset.py          # Download from Hugging Face
│   │   ├── clean_dataset.py             # Clean and categorize resumes
│   │   └── process_all_resumes.py       # NLP processing pipeline
│   ├── tests/                           # Unit tests
│   ├── uploads/                         # User-uploaded resumes
│   ├── requirements.txt                 # Python dependencies
│   └── README.md                        # This file
├── frontend/                            # React application (Phase 5-6)
└── docs/                                # Project documentation
```

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 16+** and **npm** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads/)

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd intelligent-career-platform
```

### 2. Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

#### Create Python Virtual Environment

```bash
python -m venv career_platform_env
```

#### Activate Virtual Environment

**On macOS/Linux:**
```bash
source career_platform_env/bin/activate
```

**On Windows:**
```bash
career_platform_env\Scripts\activate
```

#### Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Download spaCy Model

```bash
python -m spacy download en_core_web_sm
```

#### Seed Job Roles Database

```bash
python scripts/seed_job_roles.py
```

This will create the SQLite database and populate it with 10 job roles (AI Engineer, ML Engineer, Data Scientist, DevOps Engineer, etc.)

#### Configure Environment Variables (Optional)

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=sqlite:///./career_ai.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Frontend Setup

Open a new terminal and navigate to the frontend directory:

```bash
cd frontend
```

#### Install Node Dependencies

```bash
npm install
```

The frontend is pre-configured to connect to the backend at `http://localhost:8000`.

## Dependencies (requirements.txt)

```
fastapi==0.115.5
uvicorn==0.32.1
sqlalchemy==2.0.35
pydantic==2.9.2
python-multipart==0.0.6
bcrypt==4.1.2
python-jose[cryptography]==3.3.0
passlib==1.7.4
spacy==3.7.2
scikit-learn==1.5.2
pandas==2.2.3
PyPDF2==3.0.1
python-docx==1.1.0
nltk==3.8.1
joblib==1.4.2
python-dotenv==1.0.0
datasets==2.14.5
```

## Running the Application

### Start Backend Server

From the `backend` directory with activated virtual environment:

```bash
cd backend
source career_platform_env/bin/activate  # On Windows: career_platform_env\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend will be available at:
- **API**: http://127.0.0.1:8000
- **Swagger Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Start Frontend Development Server

From the `frontend` directory in a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at:
- **App**: http://localhost:5173

## Usage Guide

### 1. Register an Account

- Navigate to http://localhost:5173
- Click "Sign up" to create a new account
- Enter your email and password (min 8 characters)
- Submit to create your account

### 2. Upload Resume

- After logging in, you'll be directed to the upload page
- Click "Choose File" and select your resume (PDF, DOC, DOCX, or TXT)
- Click "Upload Resume" to process it
- Wait for the parsing to complete (usually 5-10 seconds)

### 3. View Dashboard

After successful upload, you'll be redirected to your dashboard showing:

- **Personal Information**: Name, email, and contact details
- **Skills Overview**: Technical and soft skills extracted from resume
- **Work History**: Professional experience with dates
- **Education**: Academic qualifications
- **Recommended Roles**: Top job role matches with suitability scores

### 4. Explore Role Details

- Click on any recommended role card to view detailed analysis
- See your **Strong Skills** that match the role requirements
- Identify **Skills to Strengthen** where you need improvement
- View **Skills to Acquire** that are currently missing
- Browse **Recommended Courses** tailored to fill your skill gaps

### 5. Take Action

- Click on course recommendations to enroll on Udemy or Coursera
- Use the skill gap insights to plan your learning path
- Upload updated resumes to track your progress

## API Documentation

Once the backend is running, access the interactive API documentation:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key Endpoints

**Authentication:**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

**Resume Processing:**
- `POST /resume/upload` - Upload and process resume
- `GET /resume/list` - Get user's uploaded resumes
- `GET /resume/{resume_id}` - Get specific resume details

**Role Recommendations:**
- `GET /roles/available` - Get all available job roles
- `GET /roles/recommendations/{resume_id}` - Get ML-powered recommendations
- `GET /roles/history` - Get recommendation history

## Available Job Roles

The platform recommends from 10 unified job roles:

1. **AI Engineer** - Artificial intelligence systems and applications
2. **Machine Learning Engineer** - ML model development and deployment
3. **Data Scientist** - Data analysis and predictive modeling
4. **Data Engineer** - Data pipelines and infrastructure
5. **DevOps/Cloud Engineer** - Cloud infrastructure and CI/CD
6. **Cybersecurity Engineer** - Security systems and protocols
7. **Backend Developer** - Server-side application development
8. **Full Stack Developer** - End-to-end web development
9. **Frontend Developer** - Client-side user interfaces
10. **Data Analyst** - Business intelligence and reporting

## Building for Production

### Backend Production Build

1. **Install production dependencies:**
```bash
pip install gunicorn
```

2. **Run with Gunicorn:**
```bash
cd backend
source career_platform_env/bin/activate
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Production Build

```bash
cd frontend
npm run build
```

The production-ready files will be in the `frontend/dist` directory. Serve these files with any static web server (nginx, Apache, or CDN).

## Deployment

### Option 1: Deploy to Heroku

**Backend:**

1. Create `Procfile` in backend directory:
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

2. Create `.gitignore` if not exists:
```
career_platform_env/
__pycache__/
*.pyc
career_ai.db
uploads/
```

3. Deploy:
```bash
cd backend
git init
git add .
git commit -m "Initial commit"
heroku create your-backend-app-name
git push heroku main
```

**Frontend:**
```bash
cd frontend
npm install -g vercel
vercel --prod
```

Update frontend API URL to point to Heroku backend URL.

### Option 2: Deploy to AWS

**Backend (EC2):**
1. Launch EC2 instance (Ubuntu 20.04 LTS)
2. SSH into instance: `ssh -i your-key.pem ubuntu@your-ec2-ip`
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```
4. Clone repository:
```bash
git clone <your-repo-url>
cd intelligent-career-platform/backend
```
5. Setup virtual environment and install dependencies
6. Create systemd service (`/etc/systemd/system/career-platform.service`):
```ini
[Unit]
Description=Career Platform API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/intelligent-career-platform/backend
Environment="PATH=/home/ubuntu/intelligent-career-platform/backend/career_platform_env/bin"
ExecStart=/home/ubuntu/intelligent-career-platform/backend/career_platform_env/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```
7. Setup nginx as reverse proxy
8. Enable HTTPS with Let's Encrypt

**Frontend (S3 + CloudFront):**
1. Build frontend: `npm run build`
2. Create S3 bucket and upload `dist` folder
3. Enable static website hosting
4. Create CloudFront distribution for HTTPS and caching
5. Update API URL in frontend to point to EC2 backend

### Option 3: Deploy to DigitalOcean App Platform

**Backend:**
1. Connect GitHub repository to DigitalOcean App Platform
2. Select backend directory
3. Configure build settings:
   - Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm && python scripts/seed_job_roles.py`
   - Run Command: `uvicorn app.main:app --host 0.0.0.0 --port 8080`
4. Set environment variables

**Frontend:**
1. Create new app from same repository
2. Select frontend directory
3. Configure build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. Update API URL environment variable

### Environment Variables for Production

**Backend (.env):**
```env
# For PostgreSQL in production (recommended over SQLite)
DATABASE_URL=postgresql://user:password@host:5432/career_platform_db

# Generate strong secret key (use: openssl rand -hex 32)
SECRET_KEY=your-very-secure-random-secret-key-here

# JWT Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Update with your frontend domain
CORS_ORIGINS=https://your-frontend-domain.com,https://www.your-frontend-domain.com
```

**Frontend (.env or config):**
```env
VITE_API_BASE_URL=https://your-backend-domain.com
```

## Troubleshooting

### spaCy Model Issues
```bash
# If model download fails
python -m spacy download en_core_web_sm --direct

# Verify model
python -c "import spacy; spacy.load('en_core_web_sm')"
```

### Dataset Download Issues
```bash
# If Hugging Face download fails, manually download:
# https://huggingface.co/datasets/datasetmaster/resumes
# Place master_resumes.jsonl in data/raw/
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf career_platform_env
python -m venv career_platform_env
source career_platform_env/bin/activate  # Windows: career_platform_env\Scripts\activate
pip install -r requirements.txt
```

### Backend Issues

**Issue: Database tables not created**
```bash
cd backend
source career_platform_env/bin/activate
python scripts/seed_job_roles.py
```

**Issue: ModuleNotFoundError**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Issue: Port 8000 already in use**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

**Issue: CORS errors**
- Verify CORS settings in [backend/app/main.py](backend/app/main.py#L20-L36)
- Ensure frontend origin is listed in `allow_origins`

### Frontend Issues

**Issue: npm install fails**
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Issue: Vite dev server won't start**
```bash
# Try different port
npm run dev -- --port 5174
```

**Issue: API calls failing**
- Ensure backend is running on http://127.0.0.1:8000
- Check browser console for error messages
- Verify API URL configuration

### Resume Parsing Issues

**Issue: Skills not extracted properly**
- Ensure resume has clear "Skills" or "Technical Skills" section
- Format skills in comma-separated or bullet-point format
- Supported formats: PDF, DOC, DOCX, TXT
- Check [resume_parser.py](backend/app/services/resume_parser.py) for recognized skill keywords

**Issue: Experience not extracted**
- Use standard date formats: MM/YYYY or Month Year (e.g., "03/2022 - 12/2023")
- Include job titles and company names
- Clearly separate experiences with line breaks
- Review [resume_parser.py:169-304](backend/app/services/resume_parser.py#L169-L304) for supported patterns

**Issue: Wrong skill categorization (e.g., Jenkins 3.5/3 in wrong section)**
- This has been fixed in [roles.py:189-192](backend/app/routers/roles.py#L189-L192)
- If issue persists, restart the backend server to load latest changes

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add your feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review API documentation at http://127.0.0.1:8000/docs
- Search existing issues on GitHub
- Open a new issue with detailed description and error logs

## Acknowledgments

- **Hugging Face** for the resume dataset
- **spaCy** team for NLP capabilities
- **FastAPI** for the robust backend framework
- **React** and **Vite** for the modern frontend experience
- **Recharts** for beautiful data visualizations
- **Udemy** and **Coursera** for course recommendations

---

**Made with care for helping job seekers find their perfect career match** 🚀