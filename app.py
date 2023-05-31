import pandas as pd
import pymysql
import streamlit as st
from DBUtils.PooledDB import PooledDB

from login_auth_ui.login import Login

pool = PooledDB(
    pymysql,
    host="127.0.0.1",
    port=3306,
    user='root',
    password='lbk369',
    db='dex_db',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)
conn = pool.connection()
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
    sql = """SELECT * FROM dex_maker_configs"""
    res = pd.read_sql(sql, conn)
    print(res)
    st.markdown(st.session_state)
    st.write(username)
