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
job_desc = st.text_area("Enter the job description", placeholder="Paste job description here")

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

custom_prompt_template = """Use the Resume and Job_desc to suggest the user if any modification is needed in the 
resume and suggest me some keywords relevant to job desc which he should add in his resume with roasting him like a 
best friend and rate his resume

resume: {all_text}
job_desc: {job_desc}
Question: {question}"""

def custom_prompt(custom_prompt_template):
    return PromptTemplate(template=custom_prompt_template, input_variables=["resume", "job_desc" ,"question"])

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
HF_TOKEN = hf_token
