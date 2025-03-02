import logging
from pathlib import Path
from typing import List, Dict
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import docx  
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class TextLoader:
    """Custom loader for plain text and Markdown files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load(self) -> List[Dict]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return [{"text": content}]

class WordLoader:
    """Custom loader for Word (.docx) files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def load(self) -> List[Dict]:
        doc = docx.Document(self.file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        content = "\n".join(full_text)
        return [{"text": content}]

class HTMLLoader:
    """Custom loader for HTML files."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        
    def load(self) -> List[Dict]:
        with open(self.file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        soup = BeautifulSoup(html_content, "html.parser")
        content = soup.get_text(separator="\n")
        return [{"text": content}]

class DocumentProcessor:
    """Handles document loading and processing for multiple file types."""
    
    def __init__(self, chunk_size: int = 7500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    
    def load_pdf(self, file_path: Path) -> List:
        """Load a PDF document."""
        try:
            logger.info(f"Loading PDF from {file_path}")
            loader = UnstructuredPDFLoader(str(file_path))
            return loader.load()
        except Exception as e:
            logger.error(f"Error loading PDF: {e}")
            raise
    
    def load_word(self, file_path: Path) -> List:
        """Load a Word (.docx) document."""
        try:
            logger.info(f"Loading Word document from {file_path}")
            loader = WordLoader(str(file_path))
            return loader.load()
        except Exception as e:
            logger.error(f"Error loading Word document: {e}")
            raise
    
    def load_html(self, file_path: Path) -> List:
        """Load an HTML document."""
        try:
            logger.info(f"Loading HTML from {file_path}")
            loader = HTMLLoader(str(file_path))
            return loader.load()
        except Exception as e:
            logger.error(f"Error loading HTML: {e}")
            raise
    
    def load_document(self, file_path: Path) -> List:
        """Dynamically load a document based on its file extension."""
        ext = file_path.suffix.lower()
        logger.info(f"Loading document {file_path} with extension {ext}")
        if ext == ".pdf":
            return self.load_pdf(file_path)
        elif ext == ".docx":
            return self.load_word(file_path)
        elif ext in [".html", ".htm"]:
            return self.load_html(file_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}")
    
    def split_documents(self, documents: List) -> List:
        """Split loaded documents into chunks."""
        try:
            logger.info("Splitting documents into chunks")
            return self.splitter.split_documents(documents)
        except Exception as e:
            logger.error(f"Error splitting documents: {e}")
            raise