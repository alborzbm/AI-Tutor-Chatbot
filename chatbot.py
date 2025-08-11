#
# Description: This script implements the core logic for the RAG-based chatbot.
# It loads the pre-built FAISS vector store, sets up a connection to a local LLM
# via Ollama, and creates a retrieval chain to answer questions based on the
# knowledge base.
#

# Use the new, recommended imports
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

def create_qa_chain():
    """
    Creates and returns a question-answering chain.
    This function initializes the necessary components: the LLM, the vector store,
    and the prompt template.
    """
    # 1. Initialize the LLM (Large Language Model)
    # We are using a local Llama 3 model run via Ollama.
    llm = Ollama(model="llama3.2:latest", base_url="http://host.docker.internal:11434")
    print("LLM initialized successfully.")

    # 2. Load the pre-built FAISS vector store
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vectorstore = FAISS.load_local(
        "faiss_index", embeddings, allow_dangerous_deserialization=True
    )
    print("Vector store loaded successfully.")

    # 3. Create a custom prompt template
    # This template guides the LLM on how to use the context to answer the question.
    prompt_template = """
    ### INSTRUCTION ###
    You are a helpful AI assistant specialized in answering questions about Artificial Intelligence based on the provided context.
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer from the context, just say that you don't know. Don't try to make up an answer.
    Your answer should be concise, in English, and directly address the user's question.

    Context: {context}

    Question: {question}

    ### RESPONSE ###
    """
    prompt = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    # 4. Create the RetrievalQA chain
    # This chain combines the retriever (from the vector store) and the LLM.
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # "stuff" is a simple method that crams all context into the prompt
        retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt},
    )
    print("QA chain created successfully.")
    return qa_chain

def main():
    """
    Main function to run the chatbot interaction loop.
    """
    # Create the question-answering chain
    qa_chain = create_qa_chain()

    print("\n--- AI Tutor Chatbot is ready! ---")
    print("Type 'exit' to quit.")

    # Interactive loop
    while True:
        question = input("\nAsk your question: ")
        if question.lower() == "exit":
            break
        
        # Get the answer from the chain
        result = qa_chain.invoke({"query": question})
        
        # Print the answer and the source documents
        print("\n### Answer ###")
        print(result["result"])
        
        # Optional: Print the source documents that the answer was based on
        print("\n--- Sources ---")
        for doc in result["source_documents"]:
            # We access metadata differently now
            source_info = doc.metadata.get('source', 'Unknown source')
            print(f"- {source_info} (Page: {doc.metadata.get('page', 'N/A')})")


if __name__ == "__main__":
    main()