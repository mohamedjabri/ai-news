import streamlit as st

st.title("📌 Your Bookmarked Articles")

if "bookmarks" not in st.session_state or len(st.session_state["bookmarks"]) == 0:
    st.write("You have no saved articles. Bookmark some from the home page!")
else:
    for i, article in enumerate(st.session_state["bookmarks"]):
        st.subheader(article["title"])
        st.write(f"🗓️ **Published:** {article['published']}")
        st.write(f"**Source:** {article['source']}")
        st.write(article["summary"])
        st.markdown(f"[Read more]({article['link']})", unsafe_allow_html=True)

        # Remove bookmark button
        if st.button("❌ Remove", key=f"remove_{i}"):
            st.session_state["bookmarks"].pop(i)
        
        st.markdown("---")