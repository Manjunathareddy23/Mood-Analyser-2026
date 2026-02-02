from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from google import genai

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Mood Analyzer", layout="centered")

# ---------- API KEY ----------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("❌ Gemini API key not found")
    st.stop()

client = genai.Client(api_key=GEMINI_API_KEY)

# ---------- FIND AVAILABLE GEMINI MODEL ----------
def get_text_model():
    for m in client.models.list():
        if "gemini" in m.name.lower():
            return m.name
    return None

MODEL_NAME = get_text_model()

if not MODEL_NAME:
    st.error("❌ No Gemini model available for this API key")
    st.stop()

# ---------- UI ----------
st.title("🧠 Mood Analyzer")
st.caption(f"Using model: `{MODEL_NAME}`")

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
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )
            st.success("Analysis complete ✅")
            st.write(response.text)

        except Exception as e:
            st.error("🚨 Gemini API error")
            st.exception(e)
