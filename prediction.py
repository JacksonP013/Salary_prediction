import streamlit as st
import pickle
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


if not firebase_admin._apps:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate("salary-prediction-f7578-a8488ffa0a90.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

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

# Clear Firestore collection on app start
def clear_firestore():
    docs = db.collection('salary_predictions').stream()
    for doc in docs:
        doc.reference.delete()

clear_firestore()  # Clear Firestore collection

def show_predict_page():
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
    education_level = st.selectbox("Education Level", education)
    job_type = st.selectbox("Job type", role)
    industry_type = st.selectbox("Industry", industry)

    experience = st.slider("Years of Experience", 0, 20, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education_level, experience, job_type, industry_type]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_edlevel.transform(X[:,1])
        X[:, 3] = le_role.transform(X[:,3])
        X[:, 4] = le_industry.transform(X[:,4])

        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

        # Store inputs and predicted salary in Firebase
        doc_ref = db.collection('salary_predictions').add({
            'country': country,
            'education_level': education_level,
            'years_of_experience': experience,
            'job_type': job_type,
            'industry_type': industry_type,
            'estimated_salary': float(salary[0])
        })

    # Display data from Firestore in a table
    st.write("## Prediction History")
    predictions = db.collection('salary_predictions').get()
    prediction_data = []
    for prediction in predictions:
        prediction_data.append(prediction.to_dict())
    
    if prediction_data:
        st.table(prediction_data)
    else:
        st.write("No predictions yet.")

# Run the app
if __name__ == '__main__':
    show_predict_page()

