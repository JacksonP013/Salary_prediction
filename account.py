import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests

if not firebase_admin._apps:
    cred = credentials.Certificate("salary-prediction-f7578-a8488ffa0a90.json")
    firebase_admin.initialize_app(cred)


def app():
    st.title('Welcome to salary prediction:')

    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''
    if 'signedout' not in st.session_state:
        st.session_state.signedout = False
    if 'signout' not in st.session_state:
        st.session_state.signout = False
    if 'email_input' not in st.session_state:
        st.session_state.email_input = ''
    if 'password_input' not in st.session_state:
        st.session_state.password_input = ''
    if 'show_login_form' not in st.session_state:
        st.session_state.show_login_form = True

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
            st.session_state.signedout = True
            st.session_state.signout = True
            st.session_state.show_login_form = False  # Hide the login form after successful login
        except:
            st.warning('Login Failed')

    def handle_sign_out():
        st.session_state.signout = False
        st.session_state.signedout = False
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

    if st.session_state.signout:
        st.text('Name ' + st.session_state.username)
        st.text('Email id: ' + st.session_state.useremail)
        if st.button('Sign out', key="signout_button"):  # Add key argument here
            handle_sign_out()


if __name__ == "__main__":
    app()
