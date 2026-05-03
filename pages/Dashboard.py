import streamlit as st
from supabase_client import supabase

# Protect page
if "user" not in st.session_state or st.session_state.user is None:
    st.warning("Please login to view history")

    if st.button("Go to Login"):
        st.switch_page("pages/Account.py")

    st.stop()

user = st.session_state.user

st.title("📂 Your History")

data = supabase.table("resume_analysis") \
    .select("*") \
    .eq("user_id", user.id) \
    .order("created_at", desc=True) \
    .execute()

if not data.data:
    st.info("No history yet")
else:
    for item in data.data:
        with st.expander(f"{item['created_at']}"):
            st.write("### Resume")
            st.write(item["resume_text"][:300])

            st.write("### Job Description")
            st.write(item["job_description"][:300])

            st.write("### Analysis")
            st.write(item["analysis"])