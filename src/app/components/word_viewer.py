"""Word viewer component for the Streamlit app."""
import streamlit as st
from docx import Document
from pathlib import Path
from typing import Optional

def extract_word_text(word_path: Path) -> str:
    """Extract text content from a Word document (.docx)."""
    try:
        doc = Document(word_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        st.error(f"Error extracting Word content: {e}")
        return ""

def render_word_viewer(word_text: Optional[str] = None):
    """Render the Word viewer with a font size control."""
    if word_text:
        # Font size control acting as a zoom feature for text
        font_size = st.slider(
            "Font Size",
            min_value=10,
            max_value=40,
            value=12,
            step=1
        )
        
        # Create an HTML container with the adjustable font size
        html_content = f"""
        <div style="font-size: {font_size}px; white-space: pre-wrap;">
            {word_text}
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
