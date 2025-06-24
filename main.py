import streamlit as st
from datetime import datetime

st.set_page_config(page_title="My Diary", layout="centered")

# Sidebar for navigation or additional features
st.sidebar.title("My Diary")
st.sidebar.markdown("Your personal thoughts, secured.")

# Main Title
st.title("📖 Daily Diary")

# Section: Add New Diary Entry
st.header("Add a New Entry")
with st.form("entry_form", clear_on_submit=True):
    entry_date = st.date_input("Date", datetime.today())
    entry_title = st.text_input("Title", "")
    entry_text = st.text_area("What's on your mind?", height=200)
    submitted = st.form_submit_button("Save Entry")

    if submitted and entry_text:
        # For demonstration, we just store it in session state (not persistent)
        if "entries" not in st.session_state:
            st.session_state.entries = []
        st.session_state.entries.append({
            "date": entry_date,
            "title": entry_title,
            "text": entry_text
        })
        st.success("Entry saved!")

st.markdown("---")

# Section: View Past Entries
st.header("📅 Past Entries")
if "entries" in st.session_state and st.session_state.entries:
    for entry in reversed(st.session_state.entries):
        with st.expander(f"{entry['date']} - {entry['title'] or 'No Title'}"):
            st.write(entry["text"])
else:
    st.info("No entries yet. Start writing your thoughts!")

# Optional: Settings or About in sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info("This is a simple diary app built with Streamlit. Your entries are stored in memory for this demo.")
