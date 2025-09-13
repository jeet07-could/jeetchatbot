import streamlit as st
import PyPDF2
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="AIzaSyCHVkMj2lCoArryOV-xQXy2PCDRwWNN3nk")

# Load model 
model = genai.GenerativeModel("gemini-2.0-flash")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_gemini(prompt, language="English"):
    # Add language instruction to prompt
    full_prompt = f"Answer in {language} language.\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text

st.title("📚 Quiz & Summary Bot (BYTE FORCE)")

# Language selection for Jharkhand people
language = st.selectbox(
    "Choose your language:",
    ["English", "Hindi", "Nagpuri", "Santali", "Mundari", "Ho", "Kurukh", "Khortha"]
)

option = st.radio("Choose input type:", ["Chapter name", "Upload PDF"])

if option == "Chapter name":
    chapter = st.text_input("Enter chapter name:")
    if st.button("Generate"):
        quiz = ask_gemini(f"Create a 5-question quiz from the chapter '{chapter}'. Keep it simple.", language)
        summary = ask_gemini(f"Summarize the chapter '{chapter}' in simple words.", language)
        st.subheader("📖 Summary")
        st.write(summary)
        st.subheader("📝 Quiz")
        st.write(quiz)

elif option == "Upload PDF":
    pdf_file = st.file_uploader("Upload your PDF", type="pdf")
    if pdf_file and st.button("Generate"):
        text = extract_text_from_pdf(pdf_file)
        quiz = ask_gemini(f"Create a 5-question quiz from this text:\n{text}", language)
        summary = ask_gemini(f"Summarize this text:\n{text}", language)
        st.subheader("📖 Summary")
        st.write(summary)
        st.subheader("📝 Quiz")
        st.write(quiz)
