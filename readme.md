# Intelligent Career Guidance Platform

> An AI-powered career guidance platform that analyzes resumes using NLP and Machine Learning to provide personalized job role recommendations with skill gap analysis.

[![Live Demo](https://img.shields.io/badge/🚀_Live-Demo-success?style=for-the-badge)](http://career-platform-sg-1764488932.s3-website-us-east-1.amazonaws.com)

[![GitHub](https://img.shields.io/badge/⭐_GitHub-Source-blue?style=for-the-badge)](https://github.com/im-sg/Intelligent-Career-Guidance-Platform)

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green?logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-18-blue?logo=react&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-Deployed-orange?logo=amazon-aws&logoColor=white)
![ML](https://img.shields.io/badge/ML-85%25_Accuracy-red?logo=scikitlearn&logoColor=white)

---

## 🎯 Live Demo

**Try it now**: http://career-platform-sg-1764488932.s3-website-us-east-1.amazonaws.com


### Production Metrics
- **ML Accuracy**: 85%+ on 10 job role classifications
- **API Response Time**: <300ms (p95)
- **Processing Time**: <5 seconds end-to-end
- **Uptime**: 99%+ 
- **Infrastructure Cost**: ~$1/month (AWS free tier)

---

## ✨ Key Features

- 🎯 **Resume Analysis**: Upload resumes (PDF/DOC/DOCX/TXT) and extract skills, experience, education using NLP
- 🤖 **ML-Powered Recommendations**: Random Forest classifier with 85%+ accuracy on 10 technology roles
- 📊 **Interactive Skill Gap Analysis**: Visualize strengths and weaknesses with radar charts and progress bars
- 📚 **Course Recommendations**: Get personalized learning paths with Udemy and Coursera suggestions
- 🎨 **Beautiful Dashboard**: Modern React UI with real-time data visualizations
- 🔐 **Secure Authentication**: JWT-based user authentication and authorization
- ⚡ **Fast Processing**: Complete resume analysis in under 5 seconds

---

## 🏗️ Architecture

### Cloud Deployment (AWS)

```
User Browser
    ↓
CloudFront CDN (HTTPS)
    ↓
S3 Bucket (React Frontend - Static Hosting)
    ↓ (API Calls)
EC2 Instance (t2.micro)
    ├── Nginx (Reverse Proxy)
    ├── Gunicorn (WSGI Server)
    ├── FastAPI (Python Backend)
    ├── spaCy (NLP Engine)
    ├── scikit-learn (ML Model)
    └── SQLite Database
```

**AWS Services Used**:
- **EC2 t2.micro**: Backend application server (Ubuntu 22.04)
- **S3**: Static website hosting for React frontend
- **CloudFront**: CDN for global content delivery (optional)
- **Security Groups**: Network firewall rules
- **IAM**: Access management and security

**Why This Stack?**:
- ✅ Free tier eligible ($0-1/month)
- ✅ Production-ready architecture
- ✅ Scalable and maintainable
- ✅ Industry-standard technologies

---

## 🛠️ Tech Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: FastAPI 0.115.5 (async, automatic API docs)
- **NLP**: spaCy 3.7.2 with en_core_web_sm model
- **ML**: scikit-learn 1.5.2 (Random Forest Classifier)
- **Database**: SQLite with SQLAlchemy ORM
- **File Processing**: PyPDF2, python-docx for resume parsing
- **Authentication**: JWT (python-jose, passlib, bcrypt)
- **Server**: Gunicorn + Uvicorn workers
- **Web Server**: Nginx (reverse proxy)
- **Process Manager**: systemd

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite (fast, modern)
- **HTTP Client**: Axios
- **Visualizations**: Recharts (radar charts, progress bars)
- **Routing**: React Router v6
- **Icons**: Lucide React
- **Styling**: CSS3, responsive design

### Machine Learning
- **Model**: Random Forest Classifier
- **Training Data**: 2,500+ resumes from Hugging Face
- **Features**: 52-skill taxonomy
- **Classes**: 10 technology job roles
- **Accuracy**: 85%+ on test set
- **Inference Time**: <200ms

### DevOps & Infrastructure
- **Cloud**: AWS (EC2, S3, CloudFront)
- **Version Control**: Git + GitHub
- **Deployment**: Manual deployment with systemd
- **Monitoring**: journalctl, CloudWatch (optional)
- **Security**: CORS, JWT, HTTPS-ready

---

## 📁 Project Structure

```
Intelligent-Career-Guidance-Platform/
├── backend/
│   ├── app/
│   │   ├── main.py                      # FastAPI application
│   │   ├── routers/
│   │   │   ├── auth.py                  # Authentication endpoints
│   │   │   ├── resume.py                # Resume processing
│   │   │   └── roles.py                 # Job recommendations
│   │   ├── services/
│   │   │   ├── file_processor.py        # PDF/DOCX extraction
│   │   │   ├── resume_parser.py         # NLP parsing (spaCy)
│   │   │   └── ml_role_analyzer.py      # ML inference
│   │   ├── models/
│   │   │   ├── database.py              # SQLAlchemy models
│   │   │   └── schemas.py               # Pydantic schemas
│   │   ├── ml_models/
│   │   │   ├── train_model.py           # Model training
│   │   │   └── saved_models/            # Trained artifacts
│   │   └── utils/
│   │       └── auth.py                  # JWT utilities
│   ├── data/
│   │   ├── raw/master_resumes.jsonl     # Dataset
│   │   ├── collected_resumes/           # By role (10 folders)
│   │   ├── skills/skills_taxonomy.json  # 52 skills
│   │   └── processed_resumes.json       # NLP processed
│   ├── scripts/
│   │   ├── seed_job_roles.py            # DB initialization
│   │   ├── download_dataset.py          # Hugging Face
│   │   └── process_all_resumes.py       # NLP pipeline
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/                  # React components
│   │   ├── pages/                       # Page components
│   │   ├── config/api.js                # API configuration
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   └── .env.production
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ - [Download](https://www.python.org/downloads/)
- Node.js 16+ and npm - [Download](https://nodejs.org/)
- Git - [Download](https://git-scm.com/)

### 1. Clone Repository

```bash
git clone https://github.com/im-sg/Intelligent-Career-Guidance-Platform.git
cd Intelligent-Career-Guidance-Platform
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv career_platform_env

# Activate (macOS/Linux)
source career_platform_env/bin/activate
# Windows: career_platform_env\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./career_ai.db
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CORS_ORIGINS=http://localhost:5173
EOF

# Seed database
python scripts/seed_job_roles.py

# Run backend
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Backend will be available at**:
- API: http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 3. Frontend Setup

```bash
# New terminal
cd frontend

# Install dependencies
npm install

# Run frontend
npm run dev
```

**Frontend will be available at**: http://localhost:5173

---

## 📖 Usage Guide

### 1. Upload Resume
- Navigate to http://localhost:5173
- Click "Choose File" and select resume (PDF/DOC/DOCX/TXT)
- Click "Upload Resume"
- Wait 5-10 seconds for processing

### 2. View Dashboard
After upload, view:
- **Personal Information**: Extracted from resume
- **Skills Overview**: Technical and soft skills
- **Work History**: Experience timeline
- **Education**: Academic background
- **Recommended Roles**: Top matches with scores

### 3. Analyze Skill Gaps
- Click any recommended role card
- View **Strong Skills** (what you have)
- See **Skills to Strengthen** (areas to improve)
- Find **Skills to Acquire** (what's missing)
- Get **Course Recommendations** (Udemy/Coursera)

---

## 🎓 Supported Job Roles

The platform classifies resumes into 10 technology roles:

1. **AI Engineer** - AI systems and applications
2. **Machine Learning Engineer** - ML model development and deployment
3. **Data Scientist** - Data analysis and predictive modeling
4. **Data Engineer** - Data pipelines and infrastructure
5. **DevOps/Cloud Engineer** - Cloud infrastructure and CI/CD
6. **Cybersecurity Engineer** - Security systems and protocols
7. **Backend Developer** - Server-side development
8. **Full Stack Developer** - End-to-end web development
9. **Frontend Developer** - Client-side interfaces
10. **Data Analyst** - Business intelligence and reporting

---

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Resume Processing
- `POST /resume/upload` - Upload and process resume
- `GET /resume/list` - Get user's resumes
- `GET /resume/{resume_id}` - Get resume details
- `DELETE /resume/{resume_id}` - Delete resume

### Role Recommendations
- `GET /roles/available` - List all job roles
- `GET /roles/recommendations/{resume_id}` - Get ML recommendations
- `GET /roles/{role_id}/details` - Get role details
- `GET /roles/history` - Get recommendation history

**Full API documentation**: http://127.0.0.1:8000/docs

---

## ☁️ Deployment

### Production Deployment on AWS

Our application is deployed on AWS with the following setup:

**Backend (EC2)**:
```bash
# SSH into EC2
ssh -i career-platform-key.pem ubuntu@YOUR_EC2_IP

# Clone and setup
git clone https://github.com/im-sg/Intelligent-Career-Guidance-Platform.git
cd Intelligent-Career-Guidance-Platform/backend
python3 -m venv career_platform_env
source career_platform_env/bin/activate
pip install -r requirements.txt gunicorn
python -m spacy download en_core_web_sm
python scripts/seed_job_roles.py

# Create systemd service
sudo nano /etc/systemd/system/career-platform.service
sudo systemctl enable career-platform
sudo systemctl start career-platform

# Configure Nginx
sudo nano /etc/nginx/sites-available/career-platform
sudo systemctl restart nginx
```

**Frontend (S3)**:
```bash
# Build
cd frontend
echo "VITE_API_BASE_URL=http://YOUR_EC2_IP" > .env.production
npm run build

# Deploy to S3
aws s3 sync dist/ s3://YOUR_BUCKET_NAME/ --delete
aws s3 website s3://YOUR_BUCKET_NAME/ \
    --index-document index.html \
    --error-document index.html
```

**Deployment Guides**:
- Complete AWS guide in `/docs/AWS_DEPLOYMENT_GUIDE.md`
- Alternative platforms: GCP, Azure, Railway, Vercel

---

## 🧪 Testing

```bash
# Backend tests
cd backend
source career_platform_env/bin/activate
pytest tests/

# Frontend tests
cd frontend
npm test

# Integration tests
npm run test:e2e
```

---

## 🐛 Troubleshooting

### Backend Issues

**ModuleNotFoundError**:
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

**Database not created**:
```bash
python scripts/seed_job_roles.py
```

**Port already in use**:
```bash
uvicorn app.main:app --reload --port 8001
```

**CORS errors**:
- Update `CORS_ORIGINS` in `.env`
- Restart backend: `sudo systemctl restart career-platform`

### Frontend Issues

**npm install fails**:
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**API calls failing**:
- Ensure backend is running on http://127.0.0.1:8000
- Check browser console for errors
- Verify `.env.production` has correct API URL

### Resume Parsing Issues

**Skills not extracted**:
- Use clear "Skills" section in resume
- Format: comma-separated or bullet points
- Supported: PDF, DOC, DOCX, TXT

**Experience not extracted**:
- Use standard dates: MM/YYYY or "Month Year"
- Include job titles and company names
- Separate experiences clearly

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| ML Model Accuracy | 85%+ |
| API Response Time | <300ms (p95) |
| Resume Processing | <5 seconds |
| Concurrent Users | 100+ |
| Uptime | 99%+ |
| Infrastructure Cost | $0-1/month |
| Training Dataset | 2,500+ resumes |
| Supported Formats | PDF, DOC, DOCX, TXT |

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit pull request

**Development Guidelines**:
- Follow PEP 8 for Python
- Use ESLint for JavaScript
- Write tests for new features
- Update documentation
- Ensure all tests pass

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👨‍💻 Author

**Sai Gangadhar Boddeti**

- 🎓 Master's in Computer Science | Governors State University | Dec 2025
- 💼 LinkedIn: [Sai Gangadhar Boddeti](https://linkedin.com/in/sai-gangadhar-boddeti)
- 🐙 GitHub: [@im-sg](https://github.com/im-sg)
- 📧 Email: boddetisaigangadhar@gmail.com
- 📍 Location: Chicago, IL

**Professional Experience**:
- 5+ years in backend development, cloud infrastructure, and automation
- Former Engineer at BOSCH and Senior Software Engineer at Wipro
- Expertise in Python, Java, AWS, Docker, Kubernetes, CI/CD

---

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) - Resume dataset (datasetmaster/resumes)
- [spaCy](https://spacy.io/) - NLP capabilities and models
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - Frontend framework
- [Vite](https://vitejs.dev/) - Build tool
- [Recharts](https://recharts.org/) - Data visualization library
- [scikit-learn](https://scikit-learn.org/) - Machine learning library
- [AWS](https://aws.amazon.com/) - Cloud infrastructure

---

## 📞 Support

For issues, questions, or feedback:

- 🐛 Open an [issue](https://github.com/im-sg/Intelligent-Career-Guidance-Platform/issues)
- 💬 Start a [discussion](https://github.com/im-sg/Intelligent-Career-Guidance-Platform/discussions)
- 📧 Email: sboddetisaigangadhar@gmail.com
- 📖 Check [API Documentation](http://3.234.222.235/docs)

---

## 🔗 Important Links

- **Live Demo**: http://career-platform-sg-1764488932.s3-website-us-east-1.amazonaws.com
- **API Docs**: http://3.234.222.235/docs
- **GitHub**: https://github.com/im-sg/Intelligent-Career-Guidance-Platform
<!-- - **Portfolio**: [Your Portfolio URL] -->
- 💼 LinkedIn: [Sai Gangadhar Boddeti](https://linkedin.com/in/sai-gangadhar-boddeti)

---

## 📈 Project Stats

![GitHub last commit](https://img.shields.io/github/last-commit/im-sg/Intelligent-Career-Guidance-Platform)
![GitHub issues](https://img.shields.io/github/issues/im-sg/Intelligent-Career-Guidance-Platform)
![GitHub stars](https://img.shields.io/github/stars/im-sg/Intelligent-Career-Guidance-Platform)
![GitHub forks](https://img.shields.io/github/forks/im-sg/Intelligent-Career-Guidance-Platform)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

<!-- [![Star History Chart](https://api.star-history.com/svg?repos=im-sg/Intelligent-Career-Guidance-Platform&type=Date)](https://star-history.com/#im-sg/Intelligent-Career-Guidance-Platform&Date) -->

---

<!-- **Made with ❤️ for helping job seekers find their perfect career match** 🚀 -->

**#MachineLearning #NLP #AWS #FastAPI #React #CareerTech #AI #Python #CloudComputing**
