from transformers import pipeline

# 🔁 Load once at startup
dialogue_model = pipeline("text-generation", model="microsoft/DialoGPT-medium")
qa_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_response(prompt):
    return dialogue_model(prompt, max_length=100)[0]["generated_text"]

def answer_question(context, question):
    return qa_model(question=question, context=context)["answer"]

def summarize_text(text):
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0]["summary_text"]
