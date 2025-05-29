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

custom_prompt_template =  """
You're the user's brutally honest best friend who is also an expert AI hiring manager. Review their resume against the job description, and give structured feedback.

Break it down like this:

1. ✅ What's Good: Highlight the strong parts of their resume.
2. ❌ What's Missing: Point out what crucial skills, experiences, or qualifications are missing — especially compared to the job description.
3. 🔧 Suggestions: Practical advice to improve weak sections (objective, projects, skills, etc).
4. 🧠 Killer Keywords to Add: Suggest relevant keywords and buzzwords from the job description that they should add to pass ATS filters and impress hiring managers.
5. 🧑‍⚖️ Friend Rating: Rate the resume out of 10 for job readiness and give a final one-liner like a bestie would.

Be clear, supportive, and a bit cheeky — like a friend who *wants them to win* but won't sugarcoat the truth.

resume: {resume}
job_desc: {job_desc}
question: {question}
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
