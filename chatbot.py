import streamlit as st
import pandas as pd
from pypdf2 import PdfReader
import openai

# Configure Streamlit with a blue theme
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f8ff;  /* Light blue background */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for uploading files
st.sidebar.title("Upload Files")
excel_file = st.sidebar.file_uploader("Upload Excel Sheet", type=["xlsx", "xls"])
pdf_files = st.sidebar.file_uploader("Upload PDF Documents", type=["pdf"], accept_multiple_files=True)

# Process uploaded files
if excel_file:
    df = pd.read_excel(excel_file)
    st.sidebar.write("Excel sheet loaded successfully.")
else:
    df = None

if pdf_files:
    pdf_texts = []
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        pdf_texts.append(text)
    st.sidebar.write("PDF documents loaded successfully.")
else:
    pdf_texts = []

# Set up OpenAI API (replace with your API key)
openai.api_key = "your-api-key-here"  # Replace with your actual OpenAI API key

# Chat interface
st.title("AI Chatbot")

# Check if files are uploaded
if not excel_file and not pdf_files:
    st.write("Please upload an Excel sheet and/or PDF documents to start.")
else:
    user_input = st.text_input("Ask a question:", placeholder="e.g., What’s in the data? or What’s in the document?")

    if user_input:
        # Determine query type using keywords
        if any(keyword in user_input.lower() for keyword in ["data", "sheet", "table", "sales"]):
            if df is not None:
                # Provide a summary of the Excel data as context
                summary = df.describe().to_string()
                context = f"Here is a summary of the data:\n{summary}"
            else:
                context = "No Excel data available."
        elif any(keyword in user_input.lower() for keyword in ["document", "pdf", "file", "policy"]):
            if pdf_texts:
                # Combine all PDF text as context
                context = " ".join(pdf_texts)
            else:
                context = "No PDF documents available."
        else:
            context = "I’m not sure how to answer that based on the uploaded files."

        # Generate response using OpenAI API
        with st.spinner("Processing your query..."):
            response = openai.Completion.create(
                engine="text-davinci-003",  # You can use other models like "gpt-3.5-turbo" with the Chat API
                prompt=f"Context: {context}\n\nQuestion: {user_input}\n\nAnswer:",
                max_tokens=150,
                temperature=0.7,
            )
            answer = response.choices[0].text.strip()

        # Display the response
        st.write("**Chatbot:**", answer)
