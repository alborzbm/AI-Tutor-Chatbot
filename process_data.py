#
# Name: Alborz Babazadeh
# Date: 2025-08-11
# Description: This script processes PDF documents from a specified folder,
# splits them into manageable text chunks, generates embeddings using a
# HuggingFace model, and saves them into a FAISS vector store for efficient
# similarity search. This creates the knowledge base for our RAG chatbot.
#

import os
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def extract_text_from_pdfs(pdf_directory: str) -> list[str]:
    """
    Extracts text from all PDF files in a given directory.
    
    Args:
        pdf_directory: The path to the directory containing PDF files.
    
    Returns:
        A list of strings, where each string is the text content of a PDF.
    """
    texts = []
    # Loop through all files in the specified directory.
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            # Open the PDF file.
            doc = fitz.open(pdf_path)
            text = ""
            # Iterate through each page of the PDF.
            for page in doc:
                # Extract text from the page and append it.
                text += page.get_text()
            texts.append(text)
            print(f"Successfully extracted text from: {filename}")
    return texts

def build_and_save_vector_store(texts: list[str], index_path: str):
    """
    Builds a FAISS vector store from text documents and saves it to disk.
    
    Args:
        texts: A list of text documents.
        index_path: The path to save the FAISS index file.
    """
    # Initialize a text splitter to break down large documents into smaller chunks.
    # chunk_size is the max size of a chunk, chunk_overlap keeps some context between chunks.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )
    # Create document objects from the raw texts.
    docs = text_splitter.create_documents(texts)
    
    print(f"\nSplit {len(texts)} documents into {len(docs)} chunks.")

    # Initialize the embedding model from HuggingFace.
    # This model converts text chunks into numerical vectors.
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create the FAISS vector store from the documents and their embeddings.
    # This is an efficient index for similarity search.
    print("\nBuilding FAISS vector store... This may take a moment.")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Save the created vector store to the local disk.
    vectorstore.save_local(index_path)
    print(f"\nVector store successfully saved to: {index_path}")


# This block runs only when the script is executed directly.
if __name__ == "__main__":
    # Define the path to the folder containing PDFs.
    pdf_folder = "knowledge_base"
    # Define the path where the final index will be saved.
    vector_store_path = "faiss_index"

    # Step 1: Extract text from all PDFs in the folder.
    extracted_texts = extract_text_from_pdfs(pdf_folder)
    
    # Step 2: If text extraction was successful, build and save the vector store.
    if extracted_texts:
        build_and_save_vector_store(extracted_texts, vector_store_path)