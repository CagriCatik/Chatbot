from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from config import config
from logging_config import logger

def process_question(question: str, vector_db, llm) -> str:
    """
    Process a user question using the vector database and the provided GPU-enabled LLM instance.
    """
    logger.info(f"Processing question: {question} using LLM instance: {llm}")
    
    # Create a prompt template for querying the retriever
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template=config["prompt_templates"]["query_prompt"],
    )

    # Build the retriever with multi-query support
    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), 
        llm,
        prompt=QUERY_PROMPT
    )

    # Create the response prompt using a chat template
    template = config["prompt_templates"]["response_prompt"]
    prompt = ChatPromptTemplate.from_template(template)

    # Construct the chain for retrieval-augmented generation
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    response = chain.invoke(question)
    logger.info("Question processed and response generated")
    return response