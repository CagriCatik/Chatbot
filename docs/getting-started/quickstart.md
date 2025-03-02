# Quick Start Guide

This guide will help you get started with **Ollama PDF RAG** quickly. Follow these steps to install, run, and interact with the application using your local machine.

---

## Prerequisites

Before running the application, ensure you have completed the following steps:

- Read the [Installation Guide](installation.md) and complete the setup.
- Start the Ollama service.
- Pull the required models by running:
  ```bash
  ollama pull llama3.2
  ollama pull nomic-embed-text
  ```

---

## Starting the Application

1. **Activate Your Virtual Environment**

   Activate your virtual environment to ensure dependencies are isolated:
   ```bash
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

2. **Start the Application**

   Launch the application by executing:
   ```bash
   python run.py
   ```

3. **Open the Web Interface**

   Open your browser and navigate to:
   ```
   http://localhost:8501
   ```

---

## Basic Usage

Once the application is running, follow these steps to interact with your PDF documents:

### 1. Upload a PDF

- Use the file uploader in the sidebar to select your PDF document.
- Alternatively, you can use the sample PDF provided with the application.

### 2. Select a Model

- Choose from the locally available Ollama models.
- The default model is set to `llama3.2`.

### 3. Ask Questions

- Type your question into the chat input field.
- Press **Enter** or click the **Send** button.
- Wait for the application to retrieve relevant context and generate a response.

### 4. Adjust Display

- Use the zoom slider to modify the PDF display for better readability.
- PDF pages are shown on the right side of the interface.

### 5. Clean Up

- When switching documents, use the **Delete Collection** feature to remove the current context.
- This ensures that new documents are processed with a clean slate.

---

## Example Usage

Here is an example workflow to get you started:

1. **Upload a PDF:**  
   For instance, upload a document on machine learning.

2. **Ask Questions:**  
   Try asking:
   - "What is the main idea of this document?"
   - "Can you explain the case study highlighted in the document?"
   - "Summarize the key findings."

The application will process your queries using the retrieval augmented generation pipeline and return relevant answers based on the PDF content.

---

## Tips

- **Start Broad:**  
  Begin with general questions to get an overview of the document's content.

- **Be Specific:**  
  For detailed insights, ask specific questions about sections or topics within the PDF.

- **Follow-Up Questions:**  
  Use follow-up queries for clarification or to dive deeper into particular topics.

- **Clear Context:**  
  Always clear the context by deleting the existing collection when switching documents to avoid interference from previous data.

---

## Next Steps

- **Advanced PDF Processing:**  
  Read the [PDF Processing Guide](../user-guide/pdf-processing.md) for more in-depth details and advanced usage options.

- **RAG Pipeline:**  
  Learn more about how the Retrieval Augmented Generation pipeline works by checking out the [RAG Pipeline Guide](../user-guide/rag-pipeline.md).

- **Chat Interface:**  
  Explore additional features of the interactive chat interface in the [Chat Interface Guide](../user-guide/chat-interface.md).

---

## Python Script Overview

The `local_ollama_rag.py` script orchestrates the entire workflow:

- **Loading and Previewing PDFs:**  
  The script loads a PDF file, previews its content, and logs the process.

- **Model Listing:**  
  It lists available Ollama models before and after processing.

- **Document Splitting:**  
  The PDF is split into text chunks using `RecursiveCharacterTextSplitter`.

- **Vector Database Creation:**  
  A vector database is created using Ollama embeddings to store the document chunks.

- **LLM Initialization:**  
  The ChatOllama LLM is initialized (with GPU support if available).

- **RAG Pipeline Setup:**  
  A MultiQueryRetriever is configured along with a RAG chain to process user queries.

- **Query Processing and Cleanup:**  
  The script processes queries and performs cleanup by deleting the vector database collection.

For further details, review the script `local_ollama_rag.py`.
