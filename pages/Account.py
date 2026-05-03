import streamlit as st
from supabase_client import supabase

st.title("🔐 Login / Signup")

mode = st.radio("Choose", ["Login", "Signup"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if mode == "Signup":
    if st.button("Create Account"):
        supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        st.success("Account created! Now login.")
        st.info(
    "📩 We've sent a verification link to your email.\n\n"
    "👉 Please check your inbox (and spam folder) and click the link to activate your account before logging in."
)
        

else:
    if st.button("Login"):
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if res.user:
            st.session_state.user = res.user
            st.success("Logged in!")

            # Redirect to Home
            st.switch_page("Home.py")
        else:
            st.error("Invalid credentials")