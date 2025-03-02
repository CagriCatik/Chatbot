# RAG Pipeline API

The RAG Pipeline is designed to integrate retrieval mechanisms with a language model (LLM) to answer questions based on retrieved document context. It leverages a multi-query retriever and a chain that sequentially processes context and questions through the LLM, ultimately parsing the output into a string response.

The RAG Pipeline integrates retrieval and generation components to enable question-answering over a document collection. It uses a vector database for document retrieval and an LLM manager that provides both the language model and the necessary prompts. The pipeline comprises two main stages:

1. **Retrieval**: Uses a multi-query retriever to fetch relevant context from the vector database.
2. **Generation**: Combines the retrieved context with the user's question through a chain that formats the query for the LLM, processes it, and parses the output into a final response.

---

## Class: RAGPipeline

The `RAGPipeline` class orchestrates the entire retrieval-augmented generation process. It is responsible for setting up the retriever, creating the processing chain, and ultimately invoking the chain to generate a response based on the user's question.

### Initialization

```python
def __init__(self, vector_db: Any, llm_manager: LLMManager):
    self.vector_db = vector_db
    self.llm_manager = llm_manager
    self.retriever = self._setup_retriever()
    self.chain = self._setup_chain()
```

- **Parameters:**
  - `vector_db`: A vector database instance that supports retrieval. This is expected to have an `as_retriever()` method.
  - `llm_manager`: An instance of `LLMManager`, which provides the language model (`llm`) and associated prompts.
  
During initialization, the RAGPipeline configures both the multi-query retriever and the processing chain using dedicated private methods.

---

### Methods

#### _setup_retriever

```python
def _setup_retriever(self) -> MultiQueryRetriever:
    """Set up the multi-query retriever."""
    try:
        return MultiQueryRetriever.from_llm(
            retriever=self.vector_db.as_retriever(),
            llm=self.llm_manager.llm,
            prompt=self.llm_manager.get_query_prompt()
        )
    except Exception as e:
        logger.error(f"Error setting up retriever: {e}")
        raise
```

- **Purpose:**  
  Initializes the multi-query retriever using the vector database and the query prompt provided by the LLM manager.
  
- **Components:**
  - **Retriever Source:** Uses `self.vector_db.as_retriever()` to access the document retrieval mechanism.
  - **LLM Integration:** The retriever is enhanced with the language model (`llm`) and a tailored prompt (`get_query_prompt()`).

- **Error Handling:**  
  Any issues during this setup are logged and re-raised.

---

#### _setup_chain

```python
def _setup_chain(self) -> Any:
    """Set up the RAG chain."""
    try:
        return (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.llm_manager.get_rag_prompt()
            | self.llm_manager.llm
            | StrOutputParser()
        )
    except Exception as e:
        logger.error(f"Error setting up chain: {e}")
        raise
```

- **Purpose:**  
  Constructs the RAG processing chain by composing several components in a pipeline:
  - **Input Structure:** A dictionary combining the retrieved context and the question.
  - **Prompt Application:** Applies the RAG-specific prompt from `llm_manager.get_rag_prompt()`.
  - **Language Model Execution:** Processes the prompt through the language model (`llm`).
  - **Output Parsing:** Parses the raw output using `StrOutputParser()` to produce a human-readable string.

- **Error Handling:**  
  Errors during chain construction are logged and re-raised.

---

#### get_response

```python
def get_response(self, question: str) -> str:
    """Get response for a question using the RAG pipeline."""
    try:
        logger.info(f"Getting response for question: {question}")
        return self.chain.invoke(question)
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        raise
```

- **Purpose:**  
  Invokes the constructed chain with a user-provided question and returns the generated response.
  
- **Parameters:**
  - `question`: The user's query as a string.

- **Operation:**  
  The method logs the query, invokes the chain (which internally retrieves context, applies the prompt, processes the LLM output, and parses the result), and returns the final answer.

- **Error Handling:**  
  Any exceptions during invocation are logged and re-raised.

---

## Configuration Options

The RAG Pipeline can be configured to suit various application requirements:

- **Vector Database Selection:**  
  The vector database instance (`vector_db`) must support retrieval operations and be compatible with the multi-query retriever interface.
  
- **LLM Manager Settings:**  
  The `LLMManager` should provide:
  - The language model (`llm`).
  - A method for retrieving a query prompt (`get_query_prompt()`).
  - A method for retrieving a RAG-specific prompt (`get_rag_prompt()`).

- **Chain Composition:**  
  The processing chain can be adjusted by modifying the components or their order (e.g., changing the prompt or output parser).

These configurations allow the pipeline to be fine-tuned for various domains and performance requirements.

---

## Error Handling

The pipeline employs robust error handling strategies:

- **Logging:**  
  Each significant step (retriever setup, chain setup, and response generation) includes logging to track execution and facilitate debugging.

- **Exception Propagation:**  
  Errors encountered during initialization, retriever setup, or chain invocation are caught, logged with a descriptive message, and re-raised to ensure that calling applications are aware of issues immediately.

---

## Usage Example

Below is an example that demonstrates how to initialize and use the RAG Pipeline to generate a response from a user query:

```python
# Import necessary classes
# from your_module import RAGPipeline, LLMManager
# Assume `vector_db` is an initialized vector database instance.

# Initialize the LLMManager with the necessary LLM and prompt configurations
llm_manager = LLMManager(
    # Provide necessary initialization parameters for your LLMManager
)

# Initialize the RAG pipeline with the vector database and LLM manager
pipeline = RAGPipeline(vector_db=vector_db, llm_manager=llm_manager)

# Process a user query and get a response
question = "What is Retrieval Augmented Generation (RAG)?"
try:
    response = pipeline.get_response(question)
    print("Response:", response)
except Exception as e:
    print(f"Failed to get response: {e}")
```

In this example, the pipeline is configured with a vector database and an LLM manager. A user query is passed to the `get_response` method, which returns the processed answer by leveraging the retrieval and generation chain.

---

## Performance Tuning

To optimize the RAG Pipeline for specific use cases, consider the following adjustments:

- **Retrieval Parameters:**  
  Fine-tune the underlying vector database settings to improve retrieval relevance.
  
- **Chain Component Adjustments:**  
  Experiment with different prompt designs or output parsers to improve response quality.
  
- **LLM Settings:**  
  Modify LLM parameters such as temperature, context window size, and response length based on the desired output characteristics.

These tuning options can help balance performance and accuracy according to application needs.
