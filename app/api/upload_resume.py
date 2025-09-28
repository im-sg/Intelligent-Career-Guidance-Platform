from fastapi import APIRouter, File, UploadFile
import pdfplumber
from app.services.resume_parser import parse_resume_text

router = APIRouter()

@router.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported."}

    contents = await file.read()

    with open("temp_resume.pdf", "wb") as f:
        f.write(contents)

    text = ""
    with pdfplumber.open("temp_resume.pdf") as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    parsed_data = parse_resume_text(text)

    return {
        "filename": file.filename,
        "parsed_data": parsed_data
    }
