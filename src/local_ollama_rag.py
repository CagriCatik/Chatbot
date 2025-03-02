import os
import subprocess
import torch
import warnings
import logging
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
    """List available Ollama models using a shell command."""
    logging.info(f"{Fore.CYAN}Listing available Ollama models...{Style.RESET_ALL}")
    try:
        subprocess.run(["ollama", "list"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error listing Ollama models: {e}")

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

def initialize_llm(model_name="deepseek-r1:14b"):
    """Initialize the ChatOllama LLM with GPU support if available."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"{Fore.MAGENTA}Using device: {device}{Style.RESET_ALL}")
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
    logging.info(f"{Fore.MAGENTA}Result:{Style.RESET_ALL}\n{Fore.LIGHTYELLOW_EX}{result}{Style.RESET_ALL}")
    return result

def clean_up(vector_db):
    """Clean up the vector database collection."""
    logging.info(f"{Fore.RED}Cleaning up: Deleting vector database collection...{Style.RESET_ALL}")
    vector_db.delete_collection()
    logging.info(f"{Fore.GREEN}Cleanup complete.{Style.RESET_ALL}")

def main():
    pdf_path = "./documents/document.pdf"
    
    try:
        # Load and preview PDF
        data = load_pdf(pdf_path)
        preview_document(data)

        # List models before processing
        list_ollama_models()

        # Split the document into chunks
        chunks = split_document(data, chunk_size=7500, chunk_overlap=100)

        # Create the vector database
        vector_db = create_vector_database(chunks)

        # List models again to verify
        list_ollama_models()

        # Initialize the LLM
        llm = initialize_llm()

        # Set up the retriever and build the chain
        retriever = setup_retriever(vector_db, llm)
        chain = build_chain(retriever, llm)

        # Process queries
        queries = [
            "What is the main idea of this document?",
            "Can you explain the case study highlighted in the document?"
        ]
        for query in queries:
            query_document(chain, query)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Cleanup vector database
        try:
            clean_up(vector_db)
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")

if __name__ == "__main__":
    main()
