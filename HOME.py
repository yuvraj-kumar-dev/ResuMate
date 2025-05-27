import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import pdfplumber
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


st.header("RESUMATE", divider=True)
st.subheader("Your AI-Powered Resume Builder")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")
job_desc = st.text_area("Enter the job description", placeholder="Paste job description here")

# Input for HUGGING_FACE API TOKEN
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

custom_prompt_template = """You're the user's brutally honest best friend who just happens to be an expert hiring manager. Review their resume against the job_desc. 
1. Roast their resume like a true friend — but give genuinely helpful, practical advice.
2. Point out where they messed up, what’s missing, and how they can fix it.
3. Suggest killer keywords that make them look like the ultimate fit for the role.
4. Give them a "Friend Rating" out of 10 for how job-ready their resume is.

resume: {resume}
job_desc: {job_desc}
question: {question}"""


prompt = PromptTemplate(
    template=custom_prompt_template,
    input_variables=["resume", "job_desc", "question"]
)

def load_llm(huggingface_repo_id):
    from langchain_huggingface import HuggingFaceEndpoint
    llm = HuggingFaceEndpoint(
        repo_id=huggingface_repo_id,
        temperature=0.5,
        huggingfacehub_api_token=hf_token,
    )
    return llm

huggingface_repo_id = "mistralai/Mistral-7B-Instruct-v0.3"


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
        st.success("Analyzed Like a Pro 🔍")
