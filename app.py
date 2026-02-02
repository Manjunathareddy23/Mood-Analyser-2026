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

# ✅ CORRECT MODEL NAME
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------- UI ----------
st.title("🧠 Mood Analyzer")
st.write("Type your feelings, let AI understand your mood")

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
            st.success("Analysis complete ✅")
            st.write(response.text)

        except Exception as e:
            st.error("🚨 Gemini API error")
            st.exception(e)
