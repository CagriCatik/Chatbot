import os
import subprocess
import torch
import warnings
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize warnings and colorama
warnings.filterwarnings('ignore')
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# Set environment variable for protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Global cache for Ollama models output
OLLAMA_MODELS_CACHE = None

def check_gpu():
    """Check and log if a GPU is available."""
    if torch.cuda.is_available():
        logging.info(f"{Fore.MAGENTA}GPU is available. Running on GPU.{Style.RESET_ALL}")
    else:
        logging.info(f"{Fore.MAGENTA}GPU not available. Running on CPU.{Style.RESET_ALL}")

def load_pdf(pdf_path: str):
    """Load a PDF document from a local file."""
    if not pdf_path or not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    logging.info(f"{Fore.CYAN}Loading PDF file: {pdf_path}{Style.RESET_ALL}")
    loader = UnstructuredPDFLoader(file_path=pdf_path)
    data = loader.load()
    logging.info(f"{Fore.GREEN}PDF loaded successfully!{Style.RESET_ALL}")
    return data

def preview_document(data, num_chars=500):
    """Print a preview of the first page of the document."""
    if not data:
        logging.error("No data to preview.")
        return
    preview_text = data[0].page_content[:num_chars]
    logging.info(f"{Fore.YELLOW}Preview of the first page:{Style.RESET_ALL}\n{Fore.BLUE}{preview_text}...{Style.RESET_ALL}")

def list_ollama_models():
    """List available Ollama models using a shell command and cache the result."""
    global OLLAMA_MODELS_CACHE
    if OLLAMA_MODELS_CACHE is not None:
        logging.info(f"{Fore.CYAN}Using cached Ollama models...{Style.RESET_ALL}")
        return OLLAMA_MODELS_CACHE

    logging.info(f"{Fore.CYAN}Listing available Ollama models...{Style.RESET_ALL}")
    try:
        result = subprocess.run(["ollama", "list"], check=True, capture_output=True, text=True)
        OLLAMA_MODELS_CACHE = result.stdout
        logging.info(f"{Fore.GREEN}Ollama models listed successfully!{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing Ollama models: {e}")
        OLLAMA_MODELS_CACHE = ""
    return OLLAMA_MODELS_CACHE

def split_document(data, chunk_size=7500, chunk_overlap=100):
    """Split the loaded PDF into text chunks."""
    logging.info(f"{Fore.CYAN}Splitting PDF into chunks (size={chunk_size}, overlap={chunk_overlap})...{Style.RESET_ALL}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(data)
    logging.info(f"{Fore.GREEN}Splitting complete. {len(chunks)} chunks created.{Style.RESET_ALL}")
    return chunks

def create_vector_database(chunks, collection_name="local-rag", embedding_model="nomic-embed-text"):
    """Create a vector database using Ollama embeddings."""
    logging.info(f"{Fore.CYAN}Creating vector database...{Style.RESET_ALL}")
    embeddings = OllamaEmbeddings(model=embedding_model)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name
    )
    logging.info(f"{Fore.GREEN}Vector database created successfully!{Style.RESET_ALL}")
    return vector_db

def initialize_llm(model_name="deepseek-r1:8b"):
    """Initialize the ChatOllama LLM with GPU support if available."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"{Fore.MAGENTA}Initializing LLM with model: {model_name} on device: {device}{Style.RESET_ALL}")
    llm = ChatOllama(model=model_name, device=device)
    return llm

def setup_retriever(vector_db, llm):
    """Setup the MultiQueryRetriever with a query prompt for generating alternative queries."""
    query_prompt = PromptTemplate(
        input_variables=["question"],
        template=(
            "You are an AI language model assistant. Your task is to generate five "
            "different versions of the given user question to retrieve relevant documents from "
            "a vector database. Provide these alternative questions separated by newlines. "
            "Original question: {question}"
        )
    )
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(),
        llm,
        prompt=query_prompt
    )
    return retriever

def build_chain(retriever, llm):
    """Construct the retrieval augmented generation (RAG) chain."""
    rag_template = (
        "Answer the question based ONLY on the following context:\n"
        "{context}\n"
        "Question: {question}\n"
    )
    prompt = ChatPromptTemplate.from_template(rag_template)
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain

def query_document(chain, query):
    """Query the document using the constructed chain and return the result."""
    logging.info(f"{Fore.CYAN}Querying document for: {query}{Style.RESET_ALL}")
    result = chain.invoke(query)
    logging.info(f"{Fore.MAGENTA}Result for query '{query}':{Style.RESET_ALL}\n{Fore.LIGHTYELLOW_EX}{result}{Style.RESET_ALL}")
    return result

def chat_with_model(prompt_text, model_name="deepseek-r1:8b"):
    """Chat with the model without uploading a document."""
    llm = initialize_llm(model_name)
    logging.info(f"{Fore.CYAN}Chatting with model: {model_name}{Style.RESET_ALL}")
    response = llm.invoke(prompt_text)
    logging.info(f"{Fore.MAGENTA}Chat response: {response}{Style.RESET_ALL}")
    return response

def clean_up(vector_db):
    """Clean up the vector database collection."""
    logging.info(f"{Fore.RED}Cleaning up: Deleting vector database collection...{Style.RESET_ALL}")
    vector_db.delete_collection()
    logging.info(f"{Fore.GREEN}Cleanup complete.{Style.RESET_ALL}")

def pdf_processing_flow():
    """Process a PDF document and handle queries using the document context."""
    start_time = time.time()
    pdf_path = "./documents/document.pdf"
    vector_db = None  # Initialize here for scope in finally

    try:
        steps = [
            "Load and preview PDF",
            "List models",
            "Split document",
            "Create vector database",
            "GPU check",
            "Initialize LLM",
            "Setup retriever and build chain",
            "Process queries"
        ]
        with tqdm(total=len(steps), desc="PDF Processing") as progress:
            # Step 1: Load and preview PDF
            data = load_pdf(pdf_path)
            preview_document(data)
            progress.update(1)

            # Step 2: List Ollama models (cached for subsequent use)
            list_ollama_models()
            progress.update(1)

            # Step 3: Split the document into chunks
            chunks = split_document(data, chunk_size=7500, chunk_overlap=100)
            progress.update(1)

            # Step 4: Create the vector database
            vector_db = create_vector_database(chunks)
            progress.update(1)

            # Step 5: GPU Check
            check_gpu()
            progress.update(1)

            # Step 6: Initialize the LLM
            llm = initialize_llm()
            progress.update(1)

            # Step 7: Set up the retriever and build the chain
            retriever = setup_retriever(vector_db, llm)
            chain = build_chain(retriever, llm)
            progress.update(1)

            # Step 8: Process queries concurrently using a ThreadPoolExecutor
            queries = [
                "What is the main idea of this document?",
                "Can you write a comprehensive documentation of the provided PDF?"
            ]
            results = []
            with ThreadPoolExecutor(max_workers=len(queries)) as executor:
                future_to_query = {executor.submit(query_document, chain, query): query for query in queries}
                for future in tqdm(as_completed(future_to_query), total=len(queries), desc="Processing queries", leave=False):
                    query = future_to_query[future]
                    try:
                        result = future.result()
                        results.append((query, result))
                    except Exception as e:
                        logging.error(f"Error processing query '{query}': {e}")
            progress.update(1)

    except Exception as e:
        logging.error(f"An error occurred during PDF processing: {e}")

    finally:
        # Cleanup vector database if it was created
        try:
            if vector_db is not None:
                clean_up(vector_db)
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
        duration = time.time() - start_time  # in seconds
        logging.info(f"{Fore.BLUE}PDF processing duration: {duration/60:.2f} minutes ({duration:.2f} seconds){Style.RESET_ALL}")

def chatbot_flow():
    """Allow the user to chat with the model directly."""
    start_time = time.time()
    try:
        check_gpu()
        # Allow the user to chat in a loop until they decide to exit.
        print("Chat with the model. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower().strip() == "exit":
                break
            response = chat_with_model(user_input)
            print(f"Chatbot: {response}")
    except Exception as e:
        logging.error(f"An error occurred during chatting: {e}")
    finally:
        duration = time.time() - start_time  # in seconds
        logging.info(f"{Fore.BLUE}Chat session duration: {duration/60:.2f} minutes ({duration:.2f} seconds){Style.RESET_ALL}")

def main():
    """Main function presenting the two-part menu."""
    print("Choose an option:")
    print("1. Upload and process a PDF file")
    print("2. Chat with Chatbot")
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        pdf_processing_flow()
    elif choice == "2":
        chatbot_flow()
    else:
        print("Invalid option selected. Please restart and choose 1 or 2.")

if __name__ == "__main__":
    main()
