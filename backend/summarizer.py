from transformers import pipeline

# Load Hugging Face summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_text(text, max_length=200):
    """Summarizes a given text using a free LLM."""
    if len(text.split()) < 100:  # Skip short texts
        return text  

    summary = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
    return summary[0]["summary_text"]