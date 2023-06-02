import numpy as np
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

from login_auth_ui.login import Login

# 创建 MySQL 连接池
db_url = 'mysql+pymysql://root:mysql@127.0.0.1:3306/dex_db?charset=utf8mb4'
engine = create_engine(db_url, pool_size=5, max_overflow=10, poolclass=QueuePool)
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
    st.markdown("Your Form Is This")
    sql = """SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = 'dex_db' AND TABLE_NAME = 'dex_maker_configs';"""
    res = pd.read_sql(sql, engine)
    res_lst = np.array(res)
    table_name = []
    for i in res_lst:
        table_name.append(str(i[0]))

    add_selectbox = st.sidebar.selectbox(
        '点击选择功能',
        ('配置信息', '监控信息', '做市状态')
    )
