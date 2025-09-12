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

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

st.title("📚 Quiz & Summary Bot (BYTE FORCE)")

option = st.radio("Choose input type:", ["Chapter name", "Upload PDF"])

if option == "Chapter name":
    chapter = st.text_input("Enter chapter name:")
    if st.button("Generate"):
        quiz = ask_gemini(f"Create a 5-question quiz from the chapter '{chapter}'. Keep it simple.")
        summary = ask_gemini(f"Summarize the chapter '{chapter}' in simple words.")
        st.subheader("📖 Summary")
        st.write(summary)
        st.subheader("📝 Quiz")
        st.write(quiz)

elif option == "Upload PDF":
    pdf_file = st.file_uploader("Upload your PDF", type="pdf")
    if pdf_file and st.button("Generate"):
        text = extract_text_from_pdf(pdf_file)
        quiz = ask_gemini(f"Create a 5-question quiz from this text:\n{text}")
        summary = ask_gemini(f"Summarize this text:\n{text}")
        st.subheader("📖 Summary")
        st.write(summary)
        st.subheader("📝 Quiz")
        st.write(quiz)
