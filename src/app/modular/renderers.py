import streamlit as st
import pdfplumber

def render_word_viewer(word_text: str):
    """Render the Word viewer with adjustable font size."""
    font_size = st.slider(
        "Font Size 🔎",
        min_value=10,
        max_value=40,
        value=12,
        step=1,
        key="docx_font_size"
    )
    html_content = f"""
    <div style="font-size: {font_size}px; white-space: pre-wrap;">
        {word_text}
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def render_html_viewer(html_content: str):
    """Render the HTML viewer with zoom controls."""
    zoom_level = st.slider(
        "HTML Zoom Level 🔎",
        min_value=50,
        max_value=200,
        value=100,
        step=10,
        key="html_zoom_slider"
    )
    zoom_factor = zoom_level / 100.0
    html_with_zoom = f"""
    <div style="transform: scale({zoom_factor}); transform-origin: top left;">
        {html_content}
    </div>
    """
    st.components.v1.html(html_with_zoom, height=600, scrolling=True)

def render_pdf_pages(file, zoom_default, zoom_min, zoom_max, zoom_step):
    """Render PDF pages with adjustable zoom level."""
    with pdfplumber.open(file) as pdf:
        pages = [page.to_image().original for page in pdf.pages]
    zoom_level = st.slider(
        "PDF Zoom Level 🔎",
        min_value=zoom_min,
        max_value=zoom_max,
        value=zoom_default,
        step=zoom_step,
        key="pdf_zoom_slider"
    )
    for page_image in pages:
        st.image(page_image, width=zoom_level)