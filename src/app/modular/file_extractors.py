import pdfplumber
from bs4 import BeautifulSoup
from docx import Document

def extract_text_from_docx(file) -> str:
    """Extract text from a DOCX file."""
    doc = Document(file)
    return "\n".join(para.text for para in doc.paragraphs)

def extract_text_from_html(file) -> str:
    """Extract plain text from an HTML file using BeautifulSoup."""
    file.seek(0)
    content = file.read().decode("utf-8")
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text()

def extract_raw_html(file) -> str:
    """Extract raw HTML content from an HTML file."""
    file.seek(0)
    return file.read().decode("utf-8")

def extract_text_from_pdf(file) -> str:
    """Extract text from a PDF file using pdfplumber."""
    with pdfplumber.open(file) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)