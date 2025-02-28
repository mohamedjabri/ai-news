import feedparser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

# List of AI-related RSS feeds
RSS_FEEDS = [
    "https://arxiv.org/rss/cs.AI",  # Arxiv AI research
    "https://huggingface.co/blog/feed.xml",  # Hugging Face blog
    "https://venturebeat.com/category/ai/feed/",  # VentureBeat AI news
    "https://www.technologyreview.com/feed/",  # MIT Tech Review (AI + Tech)
]

def get_ai_news(keyword=None):
    """Fetch AI-related news from RSS feeds and limit to 5 per source."""
    news_articles = []
    source_counts = defaultdict(int)

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            source_name = feed.feed.title  # Get source name

            # Skip source if already hit the 5-article limit
            if source_counts[source_name] >= 5:
                continue

            article = {
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary if "summary" in entry else "",
                "source": source_name,
                "published": entry.published if "published" in entry else "Unknown date",
            }

            # If filtering by keyword, only add matching articles
            if keyword:
                if keyword.lower() in entry.title.lower() or keyword.lower() in article["summary"].lower():
                    news_articles.append(article)
                    source_counts[source_name] += 1
            else:
                news_articles.append(article)
                source_counts[source_name] += 1

    return news_articles

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
