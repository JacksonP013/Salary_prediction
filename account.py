import streamlit as st
import firebase_admin
from firebase_admin import firestore, auth
from firebase_admin import credentials
import json
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate("salary-prediction-f7578-a8488ffa0a90.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def app():
    st.title('Welcome to salary prediction:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signedin' not in st.session_state:
        st.session_state.signedin = False
    if 'email_input' not in st.session_state:
        st.session_state.email_input = ''
    if 'password_input' not in st.session_state:
        st.session_state.password_input = ''
    if 'show_login_form' not in st.session_state:
        st.session_state.show_login_form = True
    if 'review_text' not in st.session_state:
        st.session_state.review_text = ''

    def sign_up_with_email_and_password(email, password, username=None, return_secure_token=True):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": return_secure_token
            }
            if username:
                payload["displayName"] = username 
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                return r.json()['email']
            except:
                st.warning(r.json())
        except Exception as e:
            st.warning(f'Signup failed: {e}')

    def sign_in_with_email_and_password(email=None, password=None, return_secure_token=True):
        rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

        try:
            payload = {
                "returnSecureToken": return_secure_token
            }
            if email:
                payload["email"] = email
            if password:
                payload["password"] = password
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            try:
                data = r.json()
                user_info = {
                    'email': data['email'],
                    'username': data.get('displayName')  # Retrieve username if available
                }
                return user_info
            except:
                st.warning(data)
        except Exception as e:
            st.warning(f'Signin failed: {e}')

    def reset_password(email):
        try:
            rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
            payload = {
                "email": email,
                "requestType": "PASSWORD_RESET"
            }
            payload = json.dumps(payload)
            r = requests.post(rest_api_url, params={"key": "AIzaSyApr-etDzcGcsVcmaw7R7rPxx3A09as7uw"}, data=payload)
            if r.status_code == 200:
                return True, "Reset email Sent"
            else:
                # Handle error response
                error_message = r.json().get('error', {}).get('message')
                return False, error_message
        except Exception as e:
            return False, str(e)

    def handle_login():
        try:
            userinfo = sign_in_with_email_and_password(st.session_state.email_input, st.session_state.password_input)
            st.session_state.username = userinfo['username']
            st.session_state.useremail = userinfo['email']
            st.session_state.signedin = True
            st.session_state.show_login_form = False  # Hide the login form after successful login
            st.experimental_rerun()
        except requests.exceptions.RequestException as e:
            st.warning('Login Failed. Please try again later or contact support.')
        except KeyError as e:
            st.warning("Incorrect email or password. Please check your credentials and try again.")
        except Exception as e:
            if isinstance(e, dict) and 'error' in e and 'message' in e['error']:
                error_message = e['error']['message']
                if error_message == 'INVALID_EMAIL':
                    st.warning("Invalid email. Please check your email address and try again.")
                elif error_message == 'INVALID_PASSWORD':
                    st.warning("Incorrect password. Please check your password and try again.")
                else:
                    st.warning(f'Login Failed. Error: {error_message}')
            else:
                st.warning('Login Failed. Please try again later or contact support.')



    def handle_sign_out():
        st.session_state.signedin = False
        st.session_state.username = ''
        st.session_state.useremail = ''
        st.session_state.show_login_form = True  # Show the login form after sign out

    def handle_password_reset():
        email = st.text_input('Email')
        if st.button('Send Reset Link'):
            success, message = reset_password(email)
            if success:
                st.success("Password reset email sent successfully.")
            else:
                st.warning(f"Password reset failed: {message}")

    def save_review(user_email, username, review_text):
        try:
            doc_ref = db.collection('reviews').document()
            doc_ref.set({
                'user_email': user_email,
                'username': username,
                'review_text': review_text
            })
            st.success("Review submitted successfully!")
        except Exception as e:
            st.warning(f"Failed to submit review: {e}")

    def display_reviews():
        st.subheader("User Reviews")
        reviews = db.collection('reviews').stream()
        for review in reviews:
            review_data = review.to_dict()
            st.write(f"Username: {review_data['username']}")
            st.write(f"Review: {review_data['review_text']}")
            st.write("---")

    if st.session_state.show_login_form:  # Show login form only if the flag is set to True
        choice = st.selectbox('Login/Signup', ['Login', 'Sign up'], key="login_choice")  # Add key argument here
        email = st.text_input('Email Address', key="email_input")  # Add key argument here
        password = st.text_input('Password', type='password', key="password_input")  # Add key argument here
        # Do not assign email to st.session_state.email_input here

        if choice == 'Sign up':
            username = st.text_input("Enter your unique username", key="username_input")  # Add key argument here
            if st.button('Create my account', key="create_account_button"):  # Add key argument here
                user = sign_up_with_email_and_password(email=email, password=password, username=username)
                st.success('Account created successfully!')
                st.markdown('Please Login using your email and password')
                st.balloons()
        else:
            if st.button('Login', key="login_button"):  # Add key argument here
                handle_login()
            handle_password_reset()

    if st.session_state.signedin:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        st.subheader("Submit Your Review")
        review_text = st.text_area("Write your review here", key="review_text_area")
        if review_text.strip():  # Check if review text is not empty or contains only whitespace
            if st.button("Submit Review"):
                save_review(st.session_state.useremail, st.session_state.username, review_text)
        else:
            st.warning("Write something...")

        display_reviews()

        if st.button("Sign out"):
            handle_sign_out()

# Run the app
app()
