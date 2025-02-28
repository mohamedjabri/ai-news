import feedparser
import streamlit as st
from collections import defaultdict

# List of AI-related RSS feeds
RSS_FEEDS = [
    "https://arxiv.org/rss/cs.AI",  # Arxiv AI research
    "https://huggingface.co/blog/feed.xml",  # Hugging Face blog
    "https://venturebeat.com/category/ai/feed/",  # VentureBeat AI news
    "https://www.technologyreview.com/feed/",  # MIT Tech Review (AI + Tech)
]

@st.cache_data(ttl=300)
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

            full_summary = entry.summary if "summary" in entry else ""

            article = {
                "title": entry.title,
                "link": entry.link,
                "summary": full_summary,
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
