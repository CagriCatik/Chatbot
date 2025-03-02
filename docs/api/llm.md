# LLM Manager API

This documentation explains the LLM Manager API, which configures the language model and manages prompt generation using Langchain’s Ollama chat models. The API simplifies the creation of dynamic prompts for query rephrasing and Retrieval Augmented Generation (RAG) tasks.

## Overview

The **LLMManager** class encapsulates:
- **LLM Configuration:** It initializes a language model using the specified model name.
- **Prompt Generation:** It provides methods to generate customized prompt templates for query refinement and RAG.

The implementation leverages:
- **ChatOllama** from `langchain_ollama.chat_models` to instantiate the language model.
- **PromptTemplate** and **ChatPromptTemplate** from `langchain.prompts` for prompt generation.

## LLMManager Class

### Class Definition

```python
class LLMManager:
    """Manages LLM configuration and prompt generation for language model interactions."""
```

### Initialization

```python
def __init__(self, model_name: str = "llama2"):
    """
    Initialize the LLMManager with a specific language model.

    Parameters:
    - model_name (str): The name of the model to be used (default is "llama2").
    """
```

**Description:**  
When instantiated, the manager sets the model name and creates a `ChatOllama` instance to handle language model interactions.

### Methods

#### get_query_prompt

```python
def get_query_prompt(self) -> PromptTemplate:
    """
    Generate a prompt template for rephrasing user questions.

    Returns:
    - A PromptTemplate configured to generate two alternative versions of the input question.
    
    Description:
    This prompt instructs the language model to provide two distinct variations of the given question. 
    These variations can help improve document retrieval by overcoming limitations of standard distance-based similarity searches.
    """
```

**Example Usage:**

```python
manager = LLMManager(model_name="llama2")
query_prompt = manager.get_query_prompt()
formatted_query = query_prompt.format(question="What is Retrieval Augmented Generation?")
print(formatted_query)
```

#### get_rag_prompt

```python
def get_rag_prompt(self) -> ChatPromptTemplate:
    """
    Create a prompt template for Retrieval Augmented Generation (RAG).

    Returns:
    - A ChatPromptTemplate tailored for generating answers based on a given context.
    
    Description:
    The template is designed to produce answers solely from the provided context. It requires:
    - `context`: The supporting information or documents.
    - `question`: The user’s query.
    """
```

**Example Usage:**

```python
rag_prompt = manager.get_rag_prompt()
formatted_rag = rag_prompt.format(context="Relevant document excerpts", question="Define RAG.")
print(formatted_rag)
```

## Usage Example

The following complete example demonstrates how to initialize the manager and generate both types of prompt templates:

```python
import logging
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate

# Optional: Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize the LLMManager
manager = LLMManager(model_name="llama2")

# Generate a query prompt template and format it
query_prompt = manager.get_query_prompt()
formatted_query = query_prompt.format(question="Explain the concept of RAG.")
print("Query Prompt:")
print(formatted_query)

# Generate a RAG prompt template and format it
rag_prompt = manager.get_rag_prompt()
formatted_rag = rag_prompt.format(context="Detailed context information here", question="What is RAG?")
print("\nRAG Prompt:")
print(formatted_rag)
```

## Logging and Error Handling

- **Logging:**  
  The module sets up a logger (`logger = logging.getLogger(__name__)`) to facilitate debugging and trace execution. Adjust the logging configuration as needed for your application.

- **Error Handling:**  
  Although the current implementation does not include explicit error handling, you should handle potential issues such as:
  - Model initialization failures.
  - Template formatting errors.
  - API communication issues.
  
  Consider extending the class to include custom error messages or exception handling where necessary.

## Model and Prompt Configuration Parameters

While the current code focuses on prompt generation, you can extend it to incorporate additional parameters for controlling language model behavior, such as:

- **Temperature:** Controls the creativity of the output.
- **Max Tokens:** Limits the response length.
- **Top_p:** Adjusts nucleus sampling.
- **Frequency Penalty:** Manages repetition in generated text.

These parameters can be integrated into future methods for text generation.

---

This enhanced documentation provides a clear and detailed guide to using the LLM Manager API, ensuring developers understand how to configure the language model and generate effective prompts for various tasks.