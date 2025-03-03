import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.auth import authenticate, load_users, save_users
from backend.summarizer import summarize_text
from backend.fetch_news import get_ai_news 
from backend.recommender import get_related_articles 
from backend.bookmarks import load_bookmarks, save_bookmarks


if "user" not in st.session_state:
    st.session_state["user"] = None

st.sidebar.title("🔑 User Login")
if st.session_state["user"]:
    st.sidebar.write(f"👋 Welcome, {st.session_state['user']}!")
    if st.sidebar.button("Logout"):
        st.session_state["user"] = None
else:
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if authenticate(username, password):
            st.session_state["user"] = username
            st.session_state["trigger_rerun"] = not st.session_state.get("trigger_rerun", False)
        else:
            st.sidebar.error("Invalid credentials!")

# Register new users
if st.sidebar.button("Create Account"):
    users = load_users()
    if username in users:
        st.sidebar.error("Username already exists!")
    else:
        users[username] = password
        save_users(users)
        st.sidebar.success("Account created! Please log in.")

st.title("📰 Daily AI News Recommender")
st.write("Get the latest AI news articles from top sources!")

if "favorites" not in st.session_state:
    st.session_state["favorites"] = set()  # Store favorite topics in session

# Load bookmarks from file
bookmarks = load_bookmarks(st.session_state['user'])
if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = bookmarks

# Input for topic selection
fav_topic = st.text_input("⭐ Add a favorite topic (e.g., LLMs, Robotics, NLP)")

if st.button("Add to Favorites"):
    if fav_topic:
        st.session_state["favorites"].add(fav_topic.lower())
        st.success(f"Added {fav_topic} to favorites!")

# Show favorite topics
if st.session_state["favorites"]:
    st.write("🎯 **Your Favorite Topics:**")
    
    # Convert set to list for display
    favorite_list = list(st.session_state["favorites"])
    
    # Display each topic with a remove button
    for topic in favorite_list:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"🔹 {topic.capitalize()}")
        with col2:
            if st.button(f"❌ Remove", key=f"remove_{topic}"):
                st.session_state["favorites"].remove(topic)

# --- Fetch News Based on Favorites ---
keyword = st.text_input("🔍 Search AI News by Keyword", "")

# If no search query, use favorite topics
if not keyword and st.session_state["favorites"]:
    keyword = " OR ".join(st.session_state["favorites"])  # Search all favorites

articles = get_ai_news(keyword)

if articles:
    for i, article in enumerate(articles):

        st.subheader(article["title"])
        st.write(f"🗓️ **Published:** {article['published']}")
        st.write(f"**Source:** {article['source']}")
        st.write("📝 **Original Summary:**")
        st.write(article["summary"])
        summarize_key = f"summarize_{i}"
        if st.button("✨ Summarize Using Bart", key=summarize_key):
            summarized_text = summarize_text(article["summary"])  # Summarize on click
            st.write("🔍 **AI-Generated Summary:**")
            st.write(summarized_text)

        st.markdown(f"[Read more]({article['link']})", unsafe_allow_html=True)

        # Get related articles
        related_articles = get_related_articles(article, [a for j, a in enumerate(articles) if j != i])

        if related_articles:
            st.write("🔗 **You might also like:**")
            for related in related_articles:
                st.markdown(f"- [{related['title']}]({related['link']})")

        # Bookmark button
        if st.button(f"⭐ Bookmark", key=f"bookmark_{i}"):
            if article["title"] not in st.session_state["bookmarks"]:
                st.session_state["bookmarks"][article["title"]] = article
                save_bookmarks(st.session_state['user'],
                               st.session_state["bookmarks"]) 
                st.success("Saved to bookmarks!")
            else:
                st.error("Article already saved! Check Bookmark Page.")

        st.markdown("---")  # Separator

else:
    st.warning("No articles found. Try a different keyword or add more favorites!")
