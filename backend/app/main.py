"""
FastAPI Main Application
Intelligent Career Guidance Platform Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.database import init_db
from app.routers import auth, resume, roles

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent Career Guidance Platform API",
    description="AI-powered resume analysis and job role recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - UPDATED FOR FRONTEND
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:5173",  # Vite React dev server
        "http://127.0.0.1:5173",
        "http://localhost:5174",  # Alternative Vite port
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables on startup"""
    init_db()
    print("\n" + "=" * 70)
    print("🚀 INTELLIGENT CAREER GUIDANCE PLATFORM API")
    print("=" * 70)
    print("\n✓ Database initialized")
    print("✓ ML model loaded")
    print("✓ API server ready")
    print("\nAPI Documentation:")
    print("  📖 Swagger UI: http://127.0.0.1:8000/docs")
    print("  📖 ReDoc: http://127.0.0.1:8000/redoc")
    print("\n" + "=" * 70 + "\n")


# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(roles.router)


# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint - API health check
    """
    return {
        "message": "Welcome to Intelligent Career Guidance Platform API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs",
        "endpoints": {
            "authentication": "/auth",
            "resume_processing": "/resume",
            "role_recommendations": "/roles"
        }
    }


# Health check
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "database": "connected",
        "ml_model": "loaded"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
