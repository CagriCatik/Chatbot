# Embeddings API Documentation

The API provides methods to generate embeddings for both documents and query texts, enabling effective semantic similarity searches.

---

## NomicEmbeddings

The `NomicEmbeddings` class is designed to manage text embeddings using Nomic's embedding model. It is primarily responsible for converting input text into numerical vector representations.

### Initialization

```python
class NomicEmbeddings:
    """Manages text embeddings using Nomic's embedding model."""
    
    def __init__(self, model_name: str = "nomic-embed-text"):
        """Initialize embeddings with model name."""
```

*By default, the model is set to `"nomic-embed-text"`, but this can be adjusted during initialization.*

---

## Methods

### embed_documents

This method generates embeddings for a list of text strings.

```python
def embed_documents(self, texts: List[str]) -> List[List[float]]:
    """Generate embeddings for a list of texts."""
```

**Parameters:**
- **`texts`**: A list of text strings.

**Returns:**
- A list where each element is an embedding vector corresponding to an input text.

---

### embed_query

This method generates an embedding for a single query text.

```python
def embed_query(self, text: str) -> List[float]:
    """Generate embedding for a single query text."""
```

**Parameters:**
- **`text`**: A query text string.

**Returns:**
- An embedding vector for the provided query.

---

## Usage Example

Below is an example demonstrating how to initialize the embeddings class and use its methods for embedding both documents and queries:

```python
# Initialize embeddings
embeddings = NomicEmbeddings()

# Embed documents
docs = ["First document", "Second document"]
doc_embeddings = embeddings.embed_documents(docs)

# Embed query
query = "Sample query"
query_embedding = embeddings.embed_query(query)
```

*This example shows how to generate embeddings for a set of documents as well as for a single query, facilitating semantic search and similarity matching.*

---

## Configuration

The embeddings component can be configured using various parameters:

- **Model Selection:** Choose the appropriate embedding model based on your requirements.
- **Batch Size:** Configure the batch size to optimize processing of multiple texts.
- **Normalization:** Apply text normalization to ensure consistent embeddings.
- **Caching Options:** Enable caching to store frequently requested embeddings for faster retrieval.

---

## Performance Optimization

To achieve optimal performance when generating embeddings, consider the following techniques:

- **Batch Processing:** Process multiple texts simultaneously to leverage computational efficiency.
- **GPU Acceleration:** Use GPU resources for faster vector computations.
- **Caching:** Cache embeddings for frequent queries to reduce computation time.
- **Dimensionality:** Monitor and adjust the dimensionality of the embeddings to balance between performance and accuracy.

---

## Best Practices

1. **Text Preparation**
   - Clean input text to remove noise.
   - Handle special characters appropriately.
   - Normalize text length to maintain consistency.

2. **Resource Management**
   - Batch process texts of similar lengths.
   - Monitor memory usage during embedding generation.
   - Cache embeddings for queries that are executed frequently.

3. **Quality Control**
   - Validate the generated embeddings for accuracy.
   - Check the dimensions of the embeddings to ensure consistency.
   - Monitor similarity scores to verify embedding quality.

---

## Python Code Implementation for Vector Store

In addition to the embeddings API, the following code snippet demonstrates vector database operations using the generated embeddings.

```python
"""Vector embeddings and database functionality."""
import logging
from typing import List
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

logger = logging.getLogger(__name__)

class VectorStore:
    """Manages vector embeddings and database operations."""
    
    def __init__(self, embedding_model: str = "nomic-embed-text"):
        self.embeddings = OllamaEmbeddings(model=embedding_model)
        self.vector_db = None
    
    def create_vector_db(self, documents: List, collection_name: str = "local-rag") -> Chroma:
        """Create vector database from documents."""
        try:
            logger.info("Creating vector database")
            self.vector_db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=collection_name
            )
            return self.vector_db
        except Exception as e:
            logger.error(f"Error creating vector database: {e}")
            raise
    
    def delete_collection(self) -> None:
        """Delete vector database collection."""
        if self.vector_db:
            try:
                logger.info("Deleting vector database collection")
                self.vector_db.delete_collection()
                self.vector_db = None
            except Exception as e:
                logger.error(f"Error deleting collection: {e}")
                raise
```

*The `VectorStore` class integrates the embedding functionality with a vector database (using Chroma) to enable efficient semantic searches and persistent storage of document embeddings.*
