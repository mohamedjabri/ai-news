from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_data(ttl=300)
def get_related_articles(main_article, all_articles, top_n=3):
    """Finds related articles using TF-IDF similarity."""
    if not all_articles:
        return []

    # Combine article titles and summaries as text
    texts = [main_article["title"] + " " + main_article["summary"]] + [
        article["title"] + " " + article["summary"] for article in all_articles
    ]

    # Convert to TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Compute cosine similarity
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    # Get top related articles
    top_indices = similarity_scores.argsort()[-top_n:][::-1]
    related_articles = [all_articles[i] for i in top_indices]

    return related_articles