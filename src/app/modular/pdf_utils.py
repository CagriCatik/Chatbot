import pdfplumber
import streamlit as st
from typing import List, Any
from logging_config import logger

@st.cache_data
def extract_all_pages_as_images(file_upload) -> List[Any]:
    """
    Extract all pages from a PDF file as images.
    """
    logger.info(f"Extracting all pages as images from file: {file_upload.name}")
    with pdfplumber.open(file_upload) as pdf:
        pdf_pages = [page.to_image().original for page in pdf.pages]
    logger.info("PDF pages extracted as images")
    return pdf_pages