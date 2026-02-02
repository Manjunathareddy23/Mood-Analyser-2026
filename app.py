from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Mood Analyzer", layout="centered")

# ---------- API KEY ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)

# ---------- MODEL ----------
model = genai.GenerativeModel("gemini-pro")

# ---------- LOAD CSS ----------
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------- UI ----------
st.markdown("<h1 class='title'>🧠 Mood Analyzer</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='subtitle'>Type your feelings, let AI understand your mood</p>",
    unsafe_allow_html=True
)

user_input = st.text_area("Enter your text", height=150)

if st.button("Analyze Mood"):
    if not user_input.strip():
        st.warning("Please enter some text")
    else:
        prompt = f"""
Analyze the emotional mood of the following text.

Respond STRICTLY in this format:
Mood:
Emotion:
Intensity (Low/Medium/High):
Advice:

Text:
{user_input}
"""

        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.4,
                    "max_output_tokens": 200
                }
            )

            st.markdown("<div class='result'>", unsafe_allow_html=True)
            st.write(response.text)
            st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error("🚨 Gemini API error")
            st.exception(e)
