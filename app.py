import streamlit as st
import firebase_admin
from firebase_admin import credentials
from prediction import show_predict_page
import account


# Check if Firebase app is already initialized
if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("salary-prediction-f7578-a8488ffa0a90.json")  # Replace with your service account key path
    firebase_admin.initialize_app(cred)

# with open('style.css') as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Function to load and display image
def load_image(image_path):
    image = open(image_path, 'rb').read()
    st.sidebar.image(image, use_column_width=True)

# Load and display image
load_image('software_Dev.jpg')

# Sidebar layout
sidebar = st.sidebar
sidebar.header('Salary Prediction')

# Text below the image
sidebar.write("The current salary prediction is based on the StackOverflow survey data for 2024. The calculations are not accurate representation of accurate salary values but rather an estimate")
sidebar.write("Developed by Jackson")

page = sidebar.selectbox("Option", ("🙍‍♂️ Account","💲  Predict"))

if page == "🙍‍♂️ Account":
    account.app()
elif page == "💲  Predict":
    show_predict_page()  # Call show_predict_page from prediction.py

