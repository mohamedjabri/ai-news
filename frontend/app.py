import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.fetch_news import get_ai_news 
from backend.recommender import get_related_articles 

st.title("📰 AI News Recommender")
st.write("Get the latest AI news articles from top sources!")

keyword = st.text_input("🔍 Search AI News by Keyword", "")
articles = get_ai_news(keyword)

if articles:
    for i, article in enumerate(articles):
        st.subheader(article["title"])
        st.write(f"🗓️ **Published:** {article['published']}")
        st.write(f"**Source:** {article['source']}")
        st.write(article["summary"])
        st.markdown(f"[Read more]({article['link']})", unsafe_allow_html=True)

        # Get related articles
        related_articles = get_related_articles(article, [a for j, a in enumerate(articles) if j != i])
        
        if related_articles:
            st.write("🔗 **You might also like:**")
            for related in related_articles:
                st.markdown(f"- [{related['title']}]({related['link']})")
        
        st.markdown("---")  # Separator

else:
    st.warning("No articles found. Try a different keyword!")
