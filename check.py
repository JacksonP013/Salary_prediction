import streamlit as st
import pickle
import numpy as np
from firebase_admin import auth, credentials, db, initialize_app
import firebase_admin

cred = credentials.Certificate("salary-prediction-f7578-a8488ffa0a90.json")
if not firebase_admin._apps:
    initialize_app(cred, {
        'databaseURL': 'https://salary-prediction-f7578-default-rtdb.firebaseio.com/'
    })

def load_model():
    with open('saved_file.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_edlevel = data["le_edlevel"]
le_role = data["le_role"]
le_industry = data["le_industry"]


firebase_db = db.reference('/comparisons')

def get_user_email():
    return st.session_state.get('user_email', None)

def show_check_page():
    user_email = get_user_email()
    if not user_email:
        st.warning("You need to be logged in to access this page.")
        st.markdown("[Go to Account Page](account.py)")
        return

    st.title("Software Developer Salary Prediction")

    st.write("""### Choose desired information and click button below""")

    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "Canada",
        "India",
        "France",
        "Netherlands",
        "Australia",
        "Brazil",
        "Spain",
        "Sweden",
        "Italy",
        "Poland",
        "Switzerland",
        "Denmark",
        "Norway",
        "Israel"
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    role ={
       'Developer, back-end', 'Developer, full-stack',
       'Developer, QA or test', 'Developer, front-end',
       'Research & Development role', 'System administrator',
       'Developer, desktop or enterprise applications',
       'Developer, embedded applications or devices',
       'Data scientist or machine learning specialist','Developer, mobile',
       'DevOps specialist', 'Database administrator',
       'Senior Executive (C-Suite, VP, etc.)', 'Data or business analyst',
       'Cloud infrastructure engineer', 'Academic researcher',
       'Engineer, data', 'Engineering manager',
       'Developer, game or graphics', 'Developer Advocate',
       'Project manager', 'Engineer, site reliability',
       'Hardware Engineer', 'Product manager', 'Security professional',
       'Scientist', 'Developer Experience',
       'Marketing or sales professional', 'Educator', 'Blockchain',
       'Designer', 'Student'
    }

    industry = {
       'Information Services, IT, Software Development, or other Technology',
       'Financial Services',
       'Manufacturing, Transportation, or Supply Chain',
       'Retail and Consumer Services', 'Higher Education', 'Insurance',
       'Healthcare', 'Wholesale', 'Oil & Gas', 'Advertising Services',
       'Legal Services'
    }

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)
    role = st.selectbox("Job type", role)
    industry = st.selectbox("Industry", industry)

    experience = st.slider("Years of Experience", 0, 20, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, experience, role, industry]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_edlevel.transform(X[:,1])
        X[:, 3] = le_role.transform(X[:,3])
        X[:, 4] = le_industry.transform(X[:,4])

        X = X.astype(float)

        predicted_salary = regressor.predict(X)[0]
        st.subheader(f"The estimated salary is ${predicted_salary:.2f}")

        inputted_salary = st.number_input("Input your salary", value=0.0)
        percentage_difference = ((predicted_salary - inputted_salary) / predicted_salary) * 100

        st.write(f"The inputted salary is {percentage_difference:.2f}% {'higher' if percentage_difference > 0 else 'lower'} than the predicted salary.")