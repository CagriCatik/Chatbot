import streamlit as st
import os
import re
import pdfplumber
import ollama
import warnings
import torch
import sys

from typing import Any, Tuple
from bs4 import BeautifulSoup
from docx import Document
from langchain.schema import HumanMessage

from config import config
from logging_config import logger
from vector_db import create_vector_db, delete_vector_db
from question_processor import process_question

# Set the log level to ERROR to avoid unnecessary logs from Ollama
os.environ["C10_LOG_LEVEL"] = "ERROR"
original_stderr = sys.stderr
sys.stderr = open(os.devnull, "w")
sys.stderr = original_stderr
warnings.filterwarnings("ignore", category=UserWarning, message=".*torch.classes.*")

# Determine device: GPU if available, else CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
if device.type == "cuda":
    logger.info("Running on GPU")
else:
    logger.info("Running on CPU")

# device = torch.device("cpu")  # Uncomment this line to force CPU usage

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

st.set_page_config(
    page_title=config["app"]["page_title"],
    layout=config["app"]["layout"],
    initial_sidebar_state=config["app"]["initial_sidebar_state"],
)

def extract_text_from_docx(file) -> str:
    """Extract text from a DOCX file."""
    doc = Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

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
        return "\n".join([page.extract_text() or "" for page in pdf.pages])

def extract_model_names(models_info: Any) -> Tuple[str, ...]:
    """Extract model names from the provided models information."""
    logger.info("Extracting model names from models_info")
    try:
        if hasattr(models_info, "models"):
            return tuple(model.model for model in models_info.models)
        return tuple()
    except Exception as e:
        logger.error(f"Error extracting model names: {e}")
        return tuple()

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

def main():
    """Main function to run the Streamlit application."""
    st.title(config["app"]["page_title"])
    st.markdown(f"### Using Device: `{device}`")

    # Get available models from Ollama
    models_info = ollama.list()
    available_models = extract_model_names(models_info)

    col1, col2 = st.columns(2)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "vector_db" not in st.session_state:
        st.session_state["vector_db"] = None

    selected_model = col1.selectbox(
        "Pick a model available locally on your system ⚙️", 
        available_models if available_models else ["default-model"],
        key="model_select"
    )

    file_upload = col1.file_uploader(
        "Upload a file (PDF, DOCX, HTML) ⬆️",
        type=["pdf", "docx", "html"],
        accept_multiple_files=False,
        key="file_uploader"
    )

    if file_upload:
        if st.session_state["vector_db"] is None:
            with st.spinner("Processing uploaded file..."):
                file_text = ""
                if file_upload.type == "application/pdf":
                    file_text = extract_text_from_pdf(file_upload)
                elif file_upload.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    file_text = extract_text_from_docx(file_upload)
                    # Save extracted DOCX text for later rendering
                    st.session_state["docx_text"] = file_text
                elif file_upload.type == "text/html":
                    # Extract plain text for vector DB and raw HTML for viewing
                    file_text = extract_text_from_html(file_upload)
                    file_upload.seek(0)
                    st.session_state["html_text"] = extract_raw_html(file_upload)

                if file_text:
                    st.session_state["vector_db"] = create_vector_db({
                        "name": file_upload.name,
                        "text": file_text
                    })
                    st.session_state["file_upload"] = file_upload
                    st.success(f"File processed: {file_upload.name}")

    # Display PDF pages if available
    if file_upload and file_upload.type == "application/pdf":
        with pdfplumber.open(file_upload) as pdf:
            st.session_state["pdf_pages"] = [page.to_image().original for page in pdf.pages]

    if "pdf_pages" in st.session_state and st.session_state["pdf_pages"]:
        zoom_level = col1.slider(
            "Zoom Level 🔎", 
            min_value=config["pdf"]["zoom_slider"]["min"], 
            max_value=config["pdf"]["zoom_slider"]["max"], 
            value=config["pdf"]["zoom_slider"]["default"], 
            step=config["pdf"]["zoom_slider"]["step"],
            key="zoom_slider"
        )
        with col1:
            with st.container(height=500, border=True):
                for page_image in st.session_state["pdf_pages"]:
                    st.image(page_image, width=zoom_level)
    
    # Render DOCX content if available
    if (file_upload and 
        file_upload.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" and 
        "docx_text" in st.session_state):
        with col1:
            st.markdown("### Word Document Viewer")
            render_word_viewer(st.session_state["docx_text"])
    
    # Render HTML content if available
    if (file_upload and 
        file_upload.type == "text/html" and 
        "html_text" in st.session_state):
        with col1:
            st.markdown("### HTML Document Viewer")
            render_html_viewer(st.session_state["html_text"])

    delete_collection = col1.button("🗑️ Delete collection", type="secondary", key="delete_button")

    if delete_collection:
        delete_vector_db(st.session_state["vector_db"])

    with col2:
        message_container = st.container(height=800, border=True)

        for message in st.session_state["messages"]:
            avatar = "🤖" if message["role"] == "assistant" else "👨🏻‍💻"
            with message_container.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])



        if prompt := st.chat_input("Enter a prompt here...", key="chat_input"):
            try:
                # Append the user prompt to the chat history
                st.session_state["messages"].append({"role": "user", "content": prompt})
                with message_container.chat_message("user", avatar="👨🏻‍💻"):
                    st.markdown(prompt)

                with message_container.chat_message("assistant", avatar="🤖"):
                    with st.spinner(":green[processing...]"):
                        from langchain_ollama.chat_models import ChatOllama
                        llm = ChatOllama(model=selected_model, device=device)
                        
                        if st.session_state.get("vector_db") is not None:
                            response = process_question(prompt, st.session_state["vector_db"], llm)
                        else:
                            user_message = HumanMessage(content=prompt)
                            response = llm.invoke([user_message])
                        
                        # If the response is a string containing metadata, extract only the reply text.
                        if isinstance(response, str):
                            # Try to extract the content between "content='" and the next "'"
                            match = re.search(r"content='(.*?)'", response)
                            if match:
                                assistant_message = match.group(1)
                            else:
                                assistant_message = response
                        elif hasattr(response, "message"):
                            assistant_message = response.message.content
                        elif isinstance(response, dict):
                            assistant_message = response.get("content", "")
                        else:
                            assistant_message = str(response)
                        
                        st.markdown(assistant_message)
                        st.session_state["messages"].append({"role": "assistant", "content": assistant_message})
                        
            except Exception as e:
                st.error(e, icon="⛔️")
                logger.error(f"Error processing prompt: {e}")

if __name__ == "__main__":
    main()