"""LLM configuration and setup."""
import logging
import textwrap
from langchain_ollama.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate, PromptTemplate

logger = logging.getLogger(__name__)

class LLMManager:
    """Manages LLM configuration and prompt templates."""

    def __init__(self, model_name: str = "llama2", llm_class=ChatOllama):
        """
        Initialize the LLMManager with a specific language model.

        Parameters:
            model_name (str): The name of the language model to use.
            llm_class (type): The class of the LLM to instantiate. Defaults to ChatOllama.
        """
        self.model_name = model_name
        try:
            self.llm = llm_class(model=model_name)
        except Exception as e:
            logger.exception("Failed to initialize LLM with model '%s'", model_name)
            raise

    def get_query_prompt(self) -> PromptTemplate:
        """
        Create a prompt template for generating query variations.

        Returns:
            PromptTemplate: A template that accepts a 'question' variable.
        """
        template = textwrap.dedent("""\
            You are an AI language model assistant. Your task is to generate 2 different versions
            of the given user question to retrieve relevant documents from a vector database.
            By generating multiple perspectives on the user question, your goal is to help the user 
            overcome some of the limitations of the distance-based similarity search.
            Provide these alternative questions separated by newlines.
            Original question: {question}
        """)
        return PromptTemplate(
            input_variables=["question"],
            template=template
        )

    def get_rag_prompt(self) -> ChatPromptTemplate:
        """
        Create a prompt template for retrieval-augmented generation (RAG).

        Returns:
            ChatPromptTemplate: A template that requires 'context' and 'question' variables.
        """
        template = textwrap.dedent("""\
            Answer the question based ONLY on the following context:
            {context}
            Question: {question}
        """)
        return ChatPromptTemplate.from_template(template)
