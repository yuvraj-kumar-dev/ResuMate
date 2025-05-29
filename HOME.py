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
import fpdf
import base64

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

custom_prompt_template = """You're the user's brutally honest best friend who also happens to be an expert hiring manager.
Your task is to review their resume in light of the job description. Please follow this **strict output format**:

###Roast:
- [Write a brutally honest but helpful roast of the resume. (2-3 sentences)]

###What is Good:
- [Highlight strengths in paragraph form.]

###What is Missing:
- [Mention gaps or missing elements in paragraph form.]

###Suggestions:
- [Give clear, actionable suggestions in paragraph form.]

###Keywords to Add:
- [List relevant keywords from the job description that should be included in the resume. (1-2 sentences)]

###Friend Rating 📊:
Score: X/10

---

resume:{resume}

job_desc:{job_desc}

question:{question}
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

def createpdf(text):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output

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
        #pdf_bytes = createpdf(response)
        #b64_pdf = base64.b64encode(pdf_bytes).decode()
        st.success("Review Complete — Ready to Level Up 🎯")
        #href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="AI_Feedback.pdf">📄 Download Feedback as PDF</a>'
        #st.markdown(href, unsafe_allow_html=True)
        
