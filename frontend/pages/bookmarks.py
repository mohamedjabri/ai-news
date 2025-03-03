import streamlit as st
from backend.bookmarks import load_bookmarks, save_bookmarks

st.title("📌 Your Bookmarked Articles")

# Load bookmarks from file
if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please log in to view your bookmarks.")
    st.stop()
bookmarks = load_bookmarks(st.session_state['user'])
if "bookmarks" not in st.session_state:
    st.session_state["bookmarks"] = bookmarks

if "bookmarks" not in st.session_state or len(st.session_state["bookmarks"]) == 0:
    st.write("You have no saved articles. Bookmark some from the home page!")
else:
    for i,( title, article) in enumerate(st.session_state["bookmarks"].items()):
        st.subheader(article["title"])
        st.write(f"🗓️ **Published:** {article['published']}")
        st.write(f"**Source:** {article['source']}")
        st.write(article["summary"])
        st.markdown(f"[Read more]({article['link']})", unsafe_allow_html=True)

        # Remove bookmark button
        if st.button("❌ Remove", key=f"remove_{i}"):
            del st.session_state["bookmarks"][title]
            save_bookmarks(st.session_state["user"], st.session_state["bookmarks"])  # Save after removing
            st.session_state["trigger_rerun"] = not st.session_state.get("trigger_rerun", False)
            st.success("Bookmark removed! Refresh the page if needed.")
        st.markdown("---")