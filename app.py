import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ---------- LOAD ENV ----------
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("Gemini API key not found. Check your .env file")
    st.stop()

# ---------- GEMINI CONFIG ----------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Mood Analyzer", layout="centered")

# ---------- LOAD CSS ----------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown("<h1 class='title'>🧠 Mood Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Type your feelings, let AI understand you</p>", unsafe_allow_html=True)

user_input = st.text_area("Enter your text", height=150)

if st.button("Analyze Mood"):
    if user_input.strip() == "":
        st.warning("Please enter some text")
    else:
        prompt = f"""
        Analyze the mood of the following text.
        Respond strictly in this format:
        Mood:
        Emotion:
        Advice:

        Text: {user_input}
        """

        response = model.generate_content(prompt)

        st.markdown("<div class='result'>", unsafe_allow_html=True)
        st.write(response.text)
        st.markdown("</div>", unsafe_allow_html=True)
