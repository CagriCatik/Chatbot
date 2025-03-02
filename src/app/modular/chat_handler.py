import re
from langchain.schema import HumanMessage
from langchain_ollama.chat_models import ChatOllama
from logging_config import logger

def extract_model_names(models_info) -> tuple:
    """Extract model names from the provided models information."""
    logger.info("Extracting model names from models_info")
    try:
        if hasattr(models_info, "models"):
            return tuple(model.model for model in models_info.models)
        return tuple()
    except Exception as e:
        logger.error(f"Error extracting model names: {e}")
        return tuple()

def process_chat(prompt: str, vector_db, selected_model, device) -> str:
    """Process the chat prompt and return the assistant's reply."""
    try:
        llm = ChatOllama(model=selected_model, device=device)
        if vector_db is not None:
            # Process the question using the vector DB
            from src.app.question_processor import process_question
            response = process_question(prompt, vector_db, llm)
        else:
            # Otherwise, simply call the language model
            user_message = HumanMessage(content=prompt)
            response = llm.invoke([user_message])
        
        # Extract the reply content from the response
        if isinstance(response, str):
            match = re.search(r"content='(.*?)'", response)
            assistant_message = match.group(1) if match else response
        elif hasattr(response, "message"):
            assistant_message = response.message.content
        elif isinstance(response, dict):
            assistant_message = response.get("content", "")
        else:
            assistant_message = str(response)
        return assistant_message

    except Exception as e:
        logger.error(f"Error processing prompt: {e}")
        raise e