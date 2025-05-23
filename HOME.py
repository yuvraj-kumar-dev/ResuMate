import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pdfplumber
import os


st.header("RESUMATE", divider=True)
st.subheader("Your AI-Powered Resume Builder")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")

# Hugging Face token input
hf_token = st.text_input("Enter your Hugging Face token", type="password")
if hf_token:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
    st.success("Hugging Face token set successfully!")

# Function to load and return documents from PDF
def extract_text_from_pdf(uploaded_file):
    all_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text

# Only run this part when a file is uploaded
if uploaded_file is not None:
    st.success(f"{uploaded_file.name} uploaded successfully!")
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", text, height=300)

# Example of how you might load your model (needs actual HuggingFace API key)
def load_llm(huggingface_repo_id):
    from langchain_huggingface import HuggingFaceEndpoint
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        huggingfacehub_api_token=hf_token,
        model_kwargs={"max_length": 512}
    )
    return llm

huggingface_repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
