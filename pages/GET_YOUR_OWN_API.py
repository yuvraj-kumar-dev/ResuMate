import streamlit as st
import requests
from streamlit_lottie import st_lottie

st.title("How to Get Your Own API")
st.write(
    "To get your own API, you need to follow these steps:"
)
st.write(
    "1. **Create an account on Hugging Face**: Go to [Hugging Face](https://huggingface.co/) and create an account if you don't have one."
) 
st.write(
    "2. **Generate an API token**: After logging in, go to your account settings and generate a new API token. This token will be used to authenticate your requests."
)
st.write(
    "3. **AFter getting the token, just paste the token in the text input box**: In the ResuMate app, there is a text input box where you can paste your Hugging Face token. This will allow the app to access the Hugging Face API and use the models available there."
)

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load the animation JSON
lottie_url = "https://lottie.host/516a1eeb-2173-4ba7-82ae-1fbf5b7f1b9c/dgM8ZzAwNL.json"
lottie_json = load_lottie_url(lottie_url)

# Display the animation
if lottie_json:
    st_lottie(lottie_json, height=300)
else:
    st.error("Failed to load animation. Please check the URL.")