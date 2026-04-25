import streamlit as st
import pdfplumber
from langchain_core.prompts import PromptTemplate
import fpdf
import base64
import re
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

st.header("RESUMATE", divider=True)
st.subheader("Your AI-Powered Resume Builder")

# Upload resume
uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf") 
mode = st.radio("Select the mode", ["Default", "ATS Optimization", "Match Score", "Rewrite Helper"])
job_desc = st.text_area("Enter the job description", placeholder="Paste job description here")



# PDF text extraction
def extract_text_from_pdf(uploaded_file):
    all_text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"
    return all_text

# Clean response text
def clean_response(text):
    text = re.sub(r'[^\u0000-\u2FFF]', '', text)
    text = re.sub(r'[\'"‘’“”«»‹›`´]', '', text)
    return text 

if uploaded_file is not None:
    st.success(f"{uploaded_file.name} uploaded successfully!")
    text = extract_text_from_pdf(uploaded_file)
    st.text_area("Extracted Text", text, height=300)

# Button style
button_style = """
    <style>
        .download-button {
            background: linear-gradient(135deg, #ff4b2b, #ff416c);
            color: white;
            padding: 12px 24px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .download-button:hover {
            background: linear-gradient(135deg, #e33e26, #e0355c);
        }
    </style>
"""

# Prompt templates
custom_prompt_template = """You're the user's brutally honest best friend who also happens to be an expert hiring manager.
Your task is to review their resume in light of the job description. Please follow this strict output format and don't use emojis and not include "assistant:" or any role tag.
Do not continue the conversation after the Friend Rating. End the response immediately after the rating.

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

###Friend Rating:
Score: X/10

---

resume:{resume}

job_desc:{job_desc}

question:{question}
"""

ats_optimization_prompt = """You're an expert in Applicant Tracking Systems (ATS) and resume parsing. Your job is to evaluate the resume's ability to pass through ATS filters based on the job description. Stick to the strict output format below. End the response after the Final Verdict.

###Section Headers:
- [Evaluate if standard ATS-readable headers like "Experience", "Education", etc. are used properly.]

###Keyword Match:
- [Analyze the presence or absence of relevant keywords from the job description.]

###Structural Recommendations:
- [Give specific tips to improve structure, layout, and scannability.]

###Final Verdict:
Pass/Fail: [State if it will likely pass ATS screening or not]

---

resume:{resume}

job_desc:{job_desc}

question:{question}
"""

match_score_prompt = """You're a resume-job matcher bot. Review the resume against the job description and provide a detailed scoring breakdown. Use the strict format below. End after the score summary.

###Match Score:
- Overall Match: X/100
- Skill Match: X/25
- Experience Match: X/25
- Keyword Match: X/25
- Role Relevance: X/25

###Keyword Density:
- Present Keywords: [List of matched keywords]
- Missing Keywords: [List of important keywords that are not present]

###Top Improvements to Increase Match:
- [Short paragraph on what to add or adjust for a better match.]

---

resume:{resume}

job_desc:{job_desc}

question:{question}
"""

rewrite_helper_prompt = """You're a top-tier professional resume writer. Rewrite the provided resume to make it more polished, concise, and effective for the job described. Use the strict format below. End after the rewrite.

###Rewritten Summary:
[Professionally rewritten version of the resume summary]

###Rewritten Experience:
[Bullet points rewritten using action verbs, impact-oriented language]

###Rewritten Skills Section:
[Optimized skill list using relevant keywords]

---

resume:{resume}

job_desc:{job_desc}

question:{question}
"""

# Choose prompt based on mode
if mode == "Default":
    prompt_given = custom_prompt_template
elif mode == "ATS Optimization":
    prompt_given = ats_optimization_prompt
elif mode == "Match Score":
    prompt_given = match_score_prompt
elif mode == "Rewrite Helper":
    prompt_given = rewrite_helper_prompt

prompt = PromptTemplate(
    template=prompt_given,
    input_variables=["resume", "job_desc", "question"]
)


def get_llm_response(prompt_text):
    llm = ChatGroq(model='llama-3.1-8b-instant')
    res = llm.invoke(prompt_text)
    return res.content

# PDF creation
def createpdf(text):
    pdf = fpdf.FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf_output = pdf.output(dest='S').encode('latin-1')
    return pdf_output

# Resume analysis
if uploaded_file and job_desc:
    question = "How can this resume be strengthened to match the job description?"
    prompt_text = prompt.format(resume=text, job_desc=job_desc, question=question)
    
    if st.button("Analyze My Resume"):
        with st.spinner("Analyzing..."):
            response = get_llm_response(prompt_text)
        
        st.subheader("Real Talk: Resume Review 💬")
        st.write(response)
        pdf_bytes = createpdf(response)
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        st.success("Review Complete — Ready to Level Up 🎯")
        href = f'''{button_style} <a href="data:application/octet-stream;base64,{b64_pdf}" 
        download="RESU-MATE_Feedback.pdf" class="download-button">📄 Download Review</a>'''
        st.markdown(href, unsafe_allow_html=True)

# Sidebar Product Hunt badge
st.sidebar.markdown(
    '<div style="position: fixed; bottom: 0; width: 20vw; min-width: 200px; z-index: 100; text-align: center; padding-bottom: 10px; background: transparent;">'
    '<a href="https://www.producthunt.com/products/prompt-master?embed=true&utm_source=badge-featured&utm_medium=badge&utm_source=badge-resumate-5" target="_blank">'
    '<img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=975004&theme=neutral&t=1749229261530" alt="ResuMate - AI that roasts your resume in ATS, HR, or expert mode | Product Hunt" style="width: 250px; height: 54px; background: transparent;" />'
    '</a>'
    '</div>',
    unsafe_allow_html=True
)

# Hide Streamlit menu/footer
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
