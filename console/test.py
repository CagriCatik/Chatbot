import re
import streamlit as st
import markdown2
from typing import List, Optional

# Enhanced regex patterns
TIMESTAMP_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?)?\s*:?.*$", re.MULTILINE)
METADATA_REGEX = re.compile(r"(?:(additional_kwargs|response_metadata|usage_metadata|id) *=? *\{.*?\}(?:\s|$))|(?:'[^']*':\s*\{.*?\})", re.DOTALL | re.IGNORECASE)
OUTPUT_REGEX = re.compile(r"^\s*Output\s*:\s*$", re.MULTILINE)
CODEBLOCK_REGEX = re.compile(r"```(?:\s*(\w+))?\s*$")
LIST_REGEX = re.compile(r"^\s*(\d+\.|-)\s+(.+)$")
KEY_VALUE_REGEX = re.compile(r"^\s*([^:>]+?)\s*:\s*(.+)$", re.MULTILINE)

def remove_metadata(text: str) -> str:
    """Remove timestamps, metadata fields, and inline metadata more aggressively."""
    text = TIMESTAMP_REGEX.sub("", text)
    text = METADATA_REGEX.sub("", text)
    return text.strip()

def format_to_markdown(input_text: str) -> str:
    """
    Improved structured Markdown formatter:
    - Thorough metadata removal
    - Cleaner thought process formatting
    - Proper code and output separation
    - Fixes escaped quotes and invalid code references
    """
    if not input_text or not input_text.strip():
        return ""

    # Initial cleanup
    text = remove_metadata(input_text)
    text = re.sub(r"<think>(.*?)</think>", r"\n### 🤔 Thought Process\n\1\n", text, flags=re.DOTALL)
    text = text.replace("\\n", "\n").replace("\\'", "'")  # Fix escaped quotes

    # Structured replacements
    text = OUTPUT_REGEX.sub("\n### 📌 Expected Output\n```\n", text)
    text = re.sub(
        r"Here's an example of Python code that uses threading:",
        "\n### 💻 Example Code\n```python\n",
        text
    )

    lines = text.splitlines()
    formatted_lines: List[str] = []
    is_in_code_block = False
    inside_output = False

    for line in lines:
        stripped_line = line.strip()

        # Skip empty lines outside code/output blocks
        if not stripped_line and not (is_in_code_block or inside_output):
            continue

        # Handle code/output blocks
        if CODEBLOCK_REGEX.match(stripped_line):
            if is_in_code_block:
                formatted_lines.append("```")
                is_in_code_block = False
                inside_output = False
            else:
                match = CODEBLOCK_REGEX.match(stripped_line)
                language = match.group(1) if match.group(1) else ("text" if inside_output else "python")
                formatted_lines.append(f"```{language}")
                is_in_code_block = True
            continue

        if is_in_code_block:
            formatted_lines.append(line)
            continue

        # Section handling
        if stripped_line.lower().startswith("chatbot:"):
            formatted_lines.append("\n### 🤖 Chatbot Response")
            continue

        if stripped_line.startswith("### 📌 Expected Output"):
            formatted_lines.append("\n### 📌 Expected Output")
            inside_output = True
            continue

        # Structured formatting
        if stripped_line.startswith("### "):
            formatted_lines.append(f"\n{stripped_line}")
            inside_output = stripped_line.startswith("### 📌 Expected Output")
        elif LIST_REGEX.match(stripped_line):
            formatted_lines.append(stripped_line)
        elif stripped_line.startswith(">"):
            formatted_lines.append(stripped_line)
        elif KEY_VALUE_REGEX.match(stripped_line) and not stripped_line.startswith(">"):
            match = KEY_VALUE_REGEX.match(stripped_line)
            key, value = match.groups()
            formatted_lines.append(f"**{key.strip()}:** {value.strip()}")
        elif stripped_line:
            formatted_lines.append(f"\n{stripped_line}")

    # Validate and fix code blocks (ensure time import if sleep is used)
    result = "\n".join(formatted_lines).strip()
    if "time.sleep" in result and "import time" not in result:
        result = result.replace("```python\n", "```python\nimport time\n")

    return result if result else "No content to format."

def display_markdown_preview(formatted_text: str) -> None:
    """Render Markdown preview with error handling."""
    st.markdown("### 📜 Formatted Markdown Preview:")
    try:
        html_output = markdown2.markdown(formatted_text, extras=["fenced-code-blocks"])
        st.markdown(html_output, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error rendering markdown: {str(e)}")

# Streamlit App
def main():
    st.title("📝 Structured Markdown Formatter")
    st.markdown("Convert chatbot responses into clean, structured Markdown.")

    user_input = st.text_area(
        "Paste your chatbot response here:",
        height=300,
        placeholder="Enter text to format...",
        key="input_area"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Format to Markdown"):
            if user_input.strip():
                formatted_output = format_to_markdown(user_input)
                st.session_state['formatted_output'] = formatted_output
                display_markdown_preview(formatted_output)
            else:
                st.warning("⚠️ Please enter some text to format.")
    
    with col2:
        if 'formatted_output' in st.session_state:
            st.download_button(
                label="📥 Download as Markdown",
                data=st.session_state['formatted_output'],
                file_name="formatted_response.md",
                mime="text/markdown",
                key="download_btn"
            )

if __name__ == "__main__":
    main()