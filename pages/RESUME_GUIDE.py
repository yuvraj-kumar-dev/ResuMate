import streamlit as st
from streamlit_lottie import st_lottie
import requests

st.title("RESUME GUIDE")

# Function to load Lottie animation
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the animation JSON
lottie_url = "https://lottie.host/262a5526-e683-4804-907f-f499ea9b563e/4KjeIZNB5n.json"
lottie_json = load_lottie_url(lottie_url)

# Display the animation
if lottie_json:
    st_lottie(lottie_json, height=300, key="resume")
else:
    st.error("Failed to load animation. Please check the URL.")

# Write resume guide content
st.write(
    "This is a guide to help you create a professional resume using the ResuMate app."
)
st.write(
    "1. **Choose a template**: The first step in creating a resume is to choose a template that suits your style and profession. "
)
st.image("C:/Users/yuvra/Downloads/Resume-Sample.jpg", caption="Sample Resume Template")
st.write(
    "2. **Fill in your details**: Once you have chosen a template, fill in your personal details, including your name, contact information, and professional summary."
)
st.write("3. **Make your RESUME in such a way that it contains relevant keywords according to the job description.")