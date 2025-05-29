import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pdfplumber
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from langchain_huggingface import HuggingFaceEndpoint

st.header("RESUMATE", divider=True)
st.subheader("Your AI-Powered Resume Builder")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")
job_desc = st.text_area("Enter the job description", placeholder="Paste job description here")

hf_token = st.text_input("Enter your Hugging Face token", type="password")
if hf_token:
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = hf_token
    st.success("Hugging Face token set successfully!")

def extract_text_from_pdf(uploaded_file):
    all_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text

if uploaded_file is not None:
    st.success(f"{uploaded_file.name} uploaded successfully!")
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", text, height=300)

custom_prompt_template =  custom_prompt_template = """
You're the user's brutally honest best friend and an expert hiring manager. Review their resume against the job description and follow the structure below:

1. **What's Good (✅):** Point out how their resume aligns with the job description.
2. **What's Missing (❌):** Mention 2–4 important gaps or mismatches with the job.
3. **Suggestions (🔧):** Give clear, actionable improvements and Suggest 5–10 high-impact keywords they should include.
4. **Friend Rating (📊):** Honestly Rate their job readiness out of 10, with a quick reason.

Keep your tone honest, precise, and supportive — like a best friend who wants them to succeed.

Resume: {resume}
Job Description: {job_desc}
Question: {question}
"""


prompt = PromptTemplate(
    template=custom_prompt_template,
    input_variables=["resume", "job_desc", "question"]
)

huggingface_repo_id = "HuggingFaceH4/zephyr-7b-beta"

def load_llm(repo_id):
    return HuggingFaceEndpoint(
        repo_id=repo_id,
        temperature=0.5,
        huggingfacehub_api_token=hf_token,
    )

if uploaded_file and job_desc and hf_token:
    llm = load_llm(huggingface_repo_id)
    question = "How can this resume be strengthened to match the job description?"
    chain = LLMChain(llm=llm, prompt=prompt)

    if st.button("Analyze My Resume"):
        with st.spinner("Analyzing..."):
            response = chain.run({
                "resume": text,
                "job_desc": job_desc,
                "question": question
            })
        st.subheader("Real Talk: Resume Review 💬")
        st.write(response)
        st.success("Review Complete — Ready to Level Up 🎯")
