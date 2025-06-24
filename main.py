import streamlit as st
from datetime import datetime
import json
import os

st.set_page_config(page_title="My Local Diary", layout="centered")
st.title("📖 Local Diary")

# --- Helper functions ---
def save_entries_to_file(entries, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def load_entries_from_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

# --- State ---
if "entries" not in st.session_state:
    st.session_state.entries = []

# --- File Upload (Load Existing Diary) ---
st.sidebar.header("Load Diary File")
uploaded_file = st.sidebar.file_uploader("Upload your diary JSON file", type="json")
if uploaded_file is not None:
    st.session_state.entries = json.load(uploaded_file)
    st.sidebar.success("Diary loaded!")

# --- File Download (Save Diary) ---
st.sidebar.header("Save Diary File")
save_filename = st.sidebar.text_input("File name to save (e.g., mydiary.json)", "mydiary.json")
if st.sidebar.button("Download Diary"):
    st.sidebar.download_button(
        label="Download",
        data=json.dumps(st.session_state.entries, ensure_ascii=False, indent=2),
        file_name=save_filename,
        mime="application/json"
    )

# --- Add New Entry ---
st.header("Add a New Entry")
with st.form("entry_form", clear_on_submit=True):
    entry_date = st.date_input("Date", datetime.today())
    entry_title = st.text_input("Title", "")
    entry_text = st.text_area("What's on your mind?", height=200)
    submitted = st.form_submit_button("Save Entry")
    if submitted and entry_text:
        st.session_state.entries.append({
            "date": entry_date.strftime("%Y-%m-%d"),
            "title": entry_title,
            "text": entry_text
        })
        st.success("Entry added!")

st.markdown("---")

# --- View Past Entries ---
st.header("📅 Past Entries")
if st.session_state.entries:
    for entry in reversed(st.session_state.entries):
        with st.expander(f"{entry['date']} - {entry['title'] or 'No Title'}"):
            st.write(entry["text"])
else:
    st.info("No entries yet. Start writing your thoughts!")

# --- About ---
st.sidebar.markdown("---")
st.sidebar.subheader("About")
st.sidebar.info(
    "Entries are only saved on your device. Use the upload/download buttons to back up or restore your diary!"
)
