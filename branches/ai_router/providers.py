import os
from transformers import pipeline
from dotenv import load_dotenv

load_dotenv()

# Optional: API keys for future cloud providers
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")

# Load HuggingFace pipelines
dialogue_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# GPT-4 (stub)
def query_openai(prompt):
    return f"[OpenAI placeholder] → '{prompt}'"

# Claude (stub)
def query_claude(prompt):
    return f"[Claude placeholder] → '{prompt}'"

# DialoGPT
def generate_response(prompt):
    try:
        return dialogue_model(prompt, max_length=100)[0]["generated_text"]
    except Exception as e:
        return f"[DialoGPT error] {str(e)}"

# DistilBERT QA
def answer_question(context, question):
    try:
        return qa_model(question=question, context=context)["answer"]
    except Exception as e:
        return f"[QA error] {str(e)}"

# BART summarization
def summarize_text(text):
    try:
        return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
    except Exception as e:
        return f"[Summarization error] {str(e)}"
