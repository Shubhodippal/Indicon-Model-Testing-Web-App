import streamlit as st
import requests

# API Base URL (Replace with your actual domain or localhost)
API_URL = "https://sers.shubhodip.in"

# Function to Sign Up User
def signup_user(username, email, phone, password):
    payload = {
        "username": username,
        "email": email,
        "phone": phone,
        "password": password
    }
    try:
        response = requests.post(f"{API_URL}/signup.php", json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Function to Log In User
def login_user(email, password):
    payload = {
        "email": email,
        "password": password
    }
    try:
        response = requests.post(f"{API_URL}/login.php", json=payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Set up Streamlit page
st.set_page_config(page_title="User Authentication", page_icon="🔐")
st.title("Speech Emotion Recognition System")

# **Initialize session state variables**
if 'page' not in st.session_state:
    st.session_state['page'] = 'Login'

# Navigation Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("Go to Signup"):
        st.session_state.page = 'Signup'
with col2:
    if st.button("Go to Login"):
        st.session_state.page = 'Login'

# Signup Page
if st.session_state.page == "Signup":
    st.header("Sign Up")
    username = st.text_input("Username")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        if username and email and phone and password:
            response = signup_user(username, email, phone, password)
            if response['status'] == "success":
                st.success("Signup successful! You can now log in.")
                st.session_state.page = 'Login'
                st.experimental_rerun()
            else:
                st.error(response['message'])
        else:
            st.warning("Please fill out all fields.")

# Login Page
if st.session_state.page == "Login":
    st.header("Log In")
    email = st.text_input("Email")
    password = st.text_input("Password", type='password')

    if st.button("Log In"):
        if email and password:
            response = login_user(email, password)
            if response['status'] == "success":
                st.success("Login successful!")
                st.session_state.username = response['username']
                st.session_state.email = response['email']
                st.info("Now go to the home page from the left side.")
            else:
                st.error(response['message'])
        else:
            st.warning("Please fill out all fields.")

# Redirect to Home Page
if st.experimental_get_query_params().get("page") == ["home"]:
    st.experimental_rerun()
