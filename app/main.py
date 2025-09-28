from fastapi import FastAPI
from app.api import upload_resume

app = FastAPI()

app.include_router(upload_resume.router)
