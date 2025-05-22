import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

st.header("RESUMATE", divider=True)
st.subheader("Your AI-Powered Resume Builder")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")
st.session_state["uploaded_file"] = uploaded_file
if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
        content = f.read()
    st.success(f"{uploaded_file.name} uploaded successfully!")

hf_token = st.text_input("Enter your Hugging Face token", type="password")
if hf_token:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
    st.success("Hugging Face token set successfully!")



