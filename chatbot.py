import streamlit as st
import PyPDF2
import google.generativeai as genai

# ---------------- CONFIG ----------------
st.set_page_config(page_title="📚 Quiz & Summary Bot", page_icon="🤖", layout="centered")

# ---------------- STYLING ----------------
st.markdown(
    """
    <style>
    /* Center all content */
    .block-container {
        max-width: 700px;
        margin: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Titles */
    h1 {
        text-align: center;
        font-size: 2rem;
        color: #2c3e50;
    }
    h2, h3 {
        color: #34495e;
    }
    /* Buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        padding: 0.8em;
        background-color: #2e86de;
        color: white;
        font-weight: 600;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #1e5ca7;
    }
    /* Input fields */
    .stTextInput>div>div>input, .stFileUploader label {
        border-radius: 10px;
    }
    /* Mobile responsiveness */
    @media (max-width: 600px) {
        h1 {
            font-size: 1.6rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- GEMINI CONFIG ----------------
genai.configure(api_key="AIzaSyCHVkMj2lCoArryOV-xQXy2PCDRwWNN3nk")
model = genai.GenerativeModel("gemini-2.0-flash")

# ---------------- FUNCTIONS ----------------
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def ask_gemini(prompt, language="English"):
    full_prompt = f"Answer in {language} language.\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text

# ---------------- APP UI ----------------
st.title("📚 Quiz & Summary Bot")
st.markdown("<p style='text-align:center;'>Powered by BYTE FORCE 🚀</p>", unsafe_allow_html=True)

# Language selection
language = st.selectbox(
    "🌐 Choose your language:",
    ["English", "Hindi", "Nagpuri", "Santali", "Mundari", "Ho", "Kurukh", "Khortha"]
)

# Input options
st.markdown("### ✨ Choose how you want to generate:")
option = st.radio("", ["📖 Chapter name", "📂 Upload PDF"], horizontal=True)

if option == "📖 Chapter name":
    chapter = st.text_input("Enter chapter name:")
    if st.button("Generate"):
        if chapter.strip():
            quiz = ask_gemini(f"Create a 5-question quiz from the chapter '{chapter}'. Keep it simple.", language)
            summary = ask_gemini(f"Summarize the chapter '{chapter}' in simple words.", language)

            st.subheader("📖 Summary")
            st.success(summary)

            st.subheader("📝 Quiz")
            st.info(quiz)
        else:
            st.warning("⚠️ Please enter a chapter name!")

elif option == "📂 Upload PDF":
    pdf_file = st.file_uploader("Upload your PDF", type="pdf")
    if pdf_file and st.button("Generate"):
        text = extract_text_from_pdf(pdf_file)
        if text.strip():
            quiz = ask_gemini(f"Create a 5-question quiz from this text:\n{text}", language)
            summary = ask_gemini(f"Summarize this text:\n{text}", language)

            st.subheader("📖 Summary")
            st.success(summary)

            st.subheader("📝 Quiz")
            st.info(quiz)
        else:
            st.error("⚠️ Could not extract text from this PDF.")
