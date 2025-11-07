"""
File processor - Extract text from PDF, DOCX, TXT
"""
import PyPDF2
import docx
from pathlib import Path


class FileProcessor:
    def __init__(self):
        """Initialize file processor"""
        pass
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from file based on type
        
        Args:
            file_path: Path to file
            file_type: File extension (.pdf, .docx, .txt)
            
        Returns:
            Extracted text as string
        """
        if file_type == ".pdf":
            return self._extract_from_pdf(file_path)
        elif file_type == ".docx":
            return self._extract_from_docx(file_path)
        elif file_type == ".txt":
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = []
        
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {e}")
        
        return "\n".join(text)
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        text = []
        
        try:
            doc = docx.Document(file_path)
            
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text.append(paragraph.text)
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {e}")
        
        return "\n".join(text)
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {e}")


if __name__ == "__main__":
    # Test file processor
    processor = FileProcessor()
    
    # Test with a sample file (if exists)
    test_file = "test_resume.txt"
    if Path(test_file).exists():
        text = processor.extract_text(test_file, ".txt")
        print(f"Extracted {len(text)} characters")
        print(text[:200])
