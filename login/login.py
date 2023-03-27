import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

hashed_passwords = stauth.Hasher(['123456']).generate()

with open('credentials.yaml') as file:
    cred = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    cred['credentials'],
    cred['cookie']['name'],
    cred['cookie']['key'],
    cred['cookie']['expiry_days'],
    cred['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    st.title('Some content')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')
    
if authentication_status:
    try:
        if authenticator.reset_password(username, 'Reset password'):
            st.success('Password modified successfully')
    except Exception as e:
        st.error(e)

try:
    if authenticator.register_user('Register user', preauthorization=False):
        st.success('User registered successfully')
except Exception as e:
    st.error(e)
    
try:
    username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
    if username_forgot_pw:
        st.success('New password sent securely')
        # Random password to be transferred to user securely
    else:
        st.error('Username not found')
except Exception as e:
    st.error(e)
    
try:
    username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
    if username_forgot_username:
        st.success('Username sent securely')
        # Username to be transferred to user securely   
    else:
        st.error('Email not found')
except Exception as e:
    st.error(e)

if authentication_status:
    try:
        if authenticator.update_user_details(username, 'Update user details'):
            st.success('Entries updated successfully')
    except Exception as e:
        st.error(e)

with open('credentials.yaml', 'w') as file:
    yaml.dump(cred, file, default_flow_style=False)