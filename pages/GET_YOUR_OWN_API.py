import streamlit as st
import requests

st.set_page_config(page_title="Hugging Face Token Guide", page_icon="🤗")

st.title("🔐 How to Get Your Hugging Face Access Token")

st.markdown("Follow these steps to securely generate your Hugging Face token:")

st.subheader("🟢 Step 1: Sign In or Sign Up")
st.markdown("""
1. Go to [huggingface.co](https://huggingface.co)
2. Click **Sign In** in the top-right corner
3. Login with GitHub/Google or create an account using email
""")

st.subheader("🟢 Step 2: Go to Access Tokens")
st.markdown("""
1. Click your profile picture (top-right)
2. Select **Settings**
3. Go to **[Access Tokens](https://huggingface.co/settings/tokens)** in the left sidebar
""")

st.subheader("🟢 Step 3: Create a New Token")
st.markdown("""
1. Click on **“New token”**
2. Set a name like `my-app-token`
3. Set role:
   - ✅ Use **Read** (recommended)
   - ❗ Use **Write** or **Admin** only if needed
4. Click **Generate**
""")

st.subheader("🟢 Step 4: Copy the Token Immediately")
st.warning("📋 You won’t be able to see this token again. Copy and store it securely.")

st.subheader("🟢 Step 5: Use the Token in Code")
st.success("Paste this token in 'Enter your Hugging Face token' field in ResuMate.")

st.success("You're now ready to use ResuMate🎉")
