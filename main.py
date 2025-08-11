#
# Description: This script creates a web service for the AI Tutor Chatbot using FastAPI.
# It exposes an endpoint to receive questions and returns AI-generated answers.
#

from fastapi import FastAPI
from pydantic import BaseModel
import chatbot

# This line MUST be at the very top level (no spaces or tabs before it)
# and the variable name MUST be 'app'.
app = FastAPI(
    title="AI Tutor Chatbot API",
    description="An API for asking questions about AI based on a curated set of research papers.",
    version="1.0.0",
)

class QuestionRequest(BaseModel):
    question: str

# This logic should also be at the top level, not inside any function.
print("Loading QA Chain... This may take a moment.")
qa_chain = chatbot.create_qa_chain()
print("QA Chain loaded successfully.")


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    Receives a question, processes it through the RAG chain, and returns the answer.
    """
    question = request.question
    result = qa_chain.invoke({"query": question})
    return {"answer": result["result"]}


@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Tutor Chatbot API. Please use the /docs endpoint to see the API documentation."}