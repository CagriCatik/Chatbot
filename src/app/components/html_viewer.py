"""HTML viewer component for the Streamlit app."""
import streamlit as st
from pathlib import Path
from typing import Optional
import streamlit.components.v1 as components

def extract_html_content(html_path: Path) -> str:
    """Extract HTML content from the given HTML file."""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"Error reading HTML file: {e}")
        return ""

def render_html_viewer(html_content: Optional[str] = None):
    """Render the HTML viewer with zoom controls."""
    if html_content:
        # HTML display controls with a slider to adjust zoom (as a percentage)
        zoom_level = st.slider(
            "Zoom Level",
            min_value=50,
            max_value=200,
            value=100,
            step=10
        )
        # Calculate the zoom factor (e.g., 100% -> 1.0, 150% -> 1.5, etc.)
        zoom_factor = zoom_level / 100.0

        # Wrap the HTML content in a div with a CSS scale transform
        html_with_zoom = f"""
        <div style="transform: scale({zoom_factor}); transform-origin: top left;">
            {html_content}
        </div>
        """
        # Render the HTML content with scrolling enabled
        components.html(html_with_zoom, height=600, scrolling=True)
