# Document Processing API 

The Document Processing API offers a robust solution for loading and processing PDF files. Built on top of the LangChain ecosystem, this API leverages the `UnstructuredPDFLoader` for reading PDF files and the `RecursiveCharacterTextSplitter` for breaking documents into manageable chunks.

The Document Processing API is designed to simplify the process of extracting text from PDF documents and preparing it for further analysis. It is particularly useful in scenarios where you need to break down large documents into smaller, context-preserving chunks.

Key features include:

- **PDF Loading**: Reads and extracts content from PDF files.
- **Document Splitting**: Divides documents into overlapping chunks to preserve context.
- **Robust Error Handling**: Logs and manages common errors such as file loading issues or problems during document splitting.

---

## Class: DocumentProcessor

The `DocumentProcessor` class encapsulates all functionality related to PDF document processing. It is implemented with clear separation of concerns, ensuring that each step—from loading to splitting—is handled with dedicated methods.

### Initialization

```python
def __init__(self, chunk_size: int = 7500, chunk_overlap: int = 100):
    self.chunk_size = chunk_size
    self.chunk_overlap = chunk_overlap
    self.splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
```

- **Parameters:**
  - `chunk_size`: Determines the number of characters in each text chunk. Default is 7500.
  - `chunk_overlap`: Specifies the number of overlapping characters between consecutive chunks to retain context. Default is 100.

Upon initialization, the class sets up the `RecursiveCharacterTextSplitter` with the provided chunking parameters, preparing it for splitting loaded documents.

---

### Methods

#### load_pdf

```python
def load_pdf(self, file_path: Path) -> List:
    """Load PDF document."""
    try:
        logger.info(f"Loading PDF from {file_path}")
        loader = UnstructuredPDFLoader(str(file_path))
        return loader.load()
    except Exception as e:
        logger.error(f"Error loading PDF: {e}")
        raise
```

- **Purpose:**  
  This method reads a PDF document from the provided file path using the `UnstructuredPDFLoader`.

- **Parameters:**
  - `file_path`: A `Path` object representing the location of the PDF file.

- **Returns:**
  - A list containing the loaded document(s).

- **Error Handling:**  
  Errors during loading (e.g., file not found or parsing errors) are logged and raised to alert the calling process.

---

#### split_documents

```python
def split_documents(self, documents: List) -> List:
    """Split documents into chunks."""
    try:
        logger.info("Splitting documents into chunks")
        return self.splitter.split_documents(documents)
    except Exception as e:
        logger.error(f"Error splitting documents: {e}")
        raise
```

- **Purpose:**  
  This method splits the provided documents into chunks using the configured text splitter.

- **Parameters:**
  - `documents`: A list of document objects to be split.

- **Returns:**
  - A new list of document chunks with the defined overlap.

- **Error Handling:**  
  Any issues encountered during the splitting process are logged and re-raised.

---

## Configuration Options

The behavior of the `DocumentProcessor` can be tailored through several parameters:

- **chunk_size**:  
  The size of each chunk in characters. This affects how finely the document is segmented.

- **chunk_overlap**:  
  The number of characters that overlap between adjacent chunks. This ensures that context is preserved across chunks.

- **Underlying Components:**  
  - `UnstructuredPDFLoader`: Used for loading and parsing PDF files.
  - `RecursiveCharacterTextSplitter`: Handles the logic of splitting the document text into chunks.

These options provide flexibility in handling a variety of PDF documents and processing requirements.

---

## Error Handling

Robust error handling is integrated within the API to ensure a reliable processing experience:

- **Logging:**  
  Informative messages are logged at each major step (loading and splitting) to facilitate debugging and monitoring.

- **Exception Management:**  
  Both methods catch exceptions, log the error details, and re-raise the exception, ensuring that any issues are not silently ignored. This approach aids in early detection of problems such as:
  - File not found errors.
  - Invalid PDF format errors.
  - Issues during the splitting process.

---

## Usage Example

Below is an example demonstrating how to utilize the `DocumentProcessor` to load and process a PDF document:

```python
from pathlib import Path
# Import DocumentProcessor from your module, for example:
# from document_processor_module import DocumentProcessor

# Initialize the document processor with desired chunking parameters
processor = DocumentProcessor(chunk_size=7500, chunk_overlap=100)

# Define the path to your PDF file
pdf_path = Path("path/to/document.pdf")

# Load the PDF document
try:
    documents = processor.load_pdf(pdf_path)
except Exception as e:
    print(f"Failed to load PDF: {e}")
    raise

# Split the loaded document into chunks
try:
    chunks = processor.split_documents(documents)
except Exception as e:
    print(f"Failed to split documents: {e}")
    raise

# Processed document chunks can now be used for further processing or analysis
for chunk in chunks:
    print(chunk.page_content)  # Assuming each chunk has a 'page_content' attribute
    print(chunk.metadata)      # And associated metadata
```

This example shows how to instantiate the processor, load a PDF, and split it into chunks while handling potential errors gracefully.
