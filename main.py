import streamlit as st
from datetime import datetime
from firebase_config import db
from emotion_model import detect_emotion

# Simulated login for now (replace with real auth later)
st.title("🔐 Welcome to MoodDiary")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
login = st.button("Login / Register")

if login:
    if email and password:
        st.session_state.user = email
        st.success(f"Logged in as {email}")
    else:
        st.error("Please enter both email and password.")

# If logged in
if "user" in st.session_state:
    st.header("📖 Add a Diary Entry")
    with st.form("entry_form", clear_on_submit=True):
        entry_date = st.date_input("Date", datetime.today())
        entry_title = st.text_input("Title", "")
        entry_text = st.text_area("What's on your mind?", height=200)
        submitted = st.form_submit_button("Save Entry")

        if submitted and entry_text:
            mood, confidence = detect_emotion(entry_text)
            entry_data = {
                "date": entry_date.strftime("%Y-%m-%d"),
                "title": entry_title,
                "text": entry_text,
                "mood": mood,
                "confidence": round(confidence, 2),
                "timestamp": datetime.now()
            }
            # Save to Firestore
            db.collection("diary").document(st.session_state.user).collection("entries").add(entry_data)
            st.success(f"Entry saved! Detected mood: **{mood}** ({confidence:.0%})")

    st.markdown("---")
    st.header("📅 Your Past Entries")

    entries_ref = db.collection("diary").document(st.session_state.user).collection("entries").order_by("timestamp", direction="DESCENDING")
    entries = entries_ref.stream()

    for entry in entries:
        e = entry.to_dict()
        with st.expander(f"{e['date']} - {e['title'] or 'No Title'} ({e['mood']})"):
            st.write(e["text"])
            st.caption(f"Mood: {e['mood']} ({e['confidence']*100:.0f}% confidence)")
else:
    st.info("Please log in to write or view your diary.")
