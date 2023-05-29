import streamlit as st

from login_auth_ui.login import Login

LoginObj = Login(
    auth_token='couries_auth_token',
    company_name='Nick',
    width=200, height=250,
    logout_button_name='Logout', hide_menu_bool=False,
    hide_footer_bool=False,
    lottie_url='https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json'
)

LOGGED_IN = LoginObj.build_login_ui()
username = LoginObj.get_username()

if LOGGED_IN == True:
    st.markdown('Your Streamlit Application Begins here!')
    st.markdown(st.session_state)
    st.write(username)
