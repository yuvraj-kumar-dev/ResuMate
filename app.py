import streamlit as st

st.header("RESUMATE", divider=True)
st.subheader("Your AI-Powered Resume Builder")

uploaded_file = st.file_uploader("Upload your resume in PDF format", type="pdf")
if uploaded_file is not None:
    with open("temp_resume.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"{uploaded_file.name} uploaded successfully!")
