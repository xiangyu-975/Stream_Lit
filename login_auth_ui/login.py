#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/15 17:54
@Author  : Nick
@File    : login.py.py
@Software: PyCharm
"""

import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu

from login_auth_ui.utils import *
from settings import ui_conf


class Login:
    """登陆模块显示完善"""

    def __init__(self, auth_token: str, company_name: str, width, height, logout_button_name: str = 'Logout',
                 hide_menu_bool: bool = False, hide_footer_bool: bool = False,
                 lottie_url: str = ui_conf):
        """
        参数含义
        :param auth_token:接收到唯一的授权令牌
        :param company_name:这是发送密码重置电子邮件的个人/组织的名称
        :param width:登陆页面动画宽度
        :param height:登陆页面动画高度
        :param logout_button_name:注销按钮
        :param hide_menu_bool:控制菜单栏是否隐藏
        :param hide_footer_bool:是否隐藏页脚
        :param lottie_url:登陆页面的动画配置
        """
        self.auth_token = auth_token
        self.company = company_name
        self.width = width
        self.height = height
        self.logout_button_name = logout_button_name
        self.hide_menu_bool = hide_menu_bool
        self.hide_footer_bool = hide_footer_bool
        self.lottie_url = lottie_url

        # 状态保持
        self.cookies = EncryptedCookieManager(
            prefix="streamlit_login_ui_yummy_cookies",
            password="2b1b2d6f-250b-d95b-5dc0-e7fd98baf66a"
        )

        if not self.cookies.ready():
            st.stop()

    def animation(self):
        """渲染页面"""
        lottie_json = self.lottie_url
        st_lottie(lottie_json, width=self.width, height=self.height)

    def sign_up_widget(self):
        """注册组件,存入json密钥"""
        with st.form("Sign Up Form"):
            name_sign_up = st.text_input('Name *', placeholder='Please enter your name')
            valid_name_check = check_valid_name(name_sign_up)

            email_sign_up = st.text_input('Email *', placeholder='Please enter your email')
            valid_email_check = check_valid_email(email_sign_up)
            unique_email_check = check_unique_email(email_sign_up)

            username_sign_up = st.text_input('Username *', placeholder='Enter a unique username')
            unique_username_check = check_unique_user(username_sign_up)

            password_sign_up = st.text_input('Password *', placeholder='Create a strong password', type='password')

            st.markdown('###')
            sign_up_submit_button = st.form_submit_button(label='Register')

            if sign_up_submit_button:
                if valid_name_check == False:
                    st.error('Please enter a valid name!')
                elif valid_email_check == False:
                    st.error('Please enter a valid Email!')
                elif unique_email_check == False:
                    st.error('Email already exists!')
                elif unique_username_check == False:
                    st.error(f'Sorry, username {username_sign_up} already exists!')
                elif unique_username_check == None:
                    st.error('Please enter a non - empty Username')

                if valid_name_check:
                    if valid_email_check:
                        if unique_username_check:
                            if unique_email_check:
                                resiger_new_str(name_sign_up, email_sign_up, username_sign_up, password_sign_up)
                                st.success('Registration Successful!')

    def get_username(self):
        """获取登陆的用户名"""
        if st.session_state['LOGOUT_BUTTON_HIT'] == False:
            fetched_cookies = self.cookies
            if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                username = fetched_cookies.get('__streamlit_login_signup_ui_username__', '')
                return username

    def login_widget(self) -> None:
        """创建登陆功能，检车用户名，密码，cookie"""
        # 检测cookie是否存在
        if st.session_state['LOGGED_IN'] == False:
            if st.session_state['LOGOUT_BUTTON_HIT'] == False:
                fetched_cookies = self.cookies
                if '__streamlit_login_signup_ui_username__' in fetched_cookies.keys():
                    if fetched_cookies.get('__streamlit_login_signup_ui_username__',
                                           '') != '8be4544f-a3d2-7e86-ca20-c914acac1bfa':
                        st.session_state['LOGGED_IN'] = True

        if st.session_state['LOGGED_IN'] == False:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

            del_login = st.empty()
            with del_login.form('Login Form'):
                username = st.text_input('Username', placeholder='Your unique username')
                password = st.text_input('Password', placeholder='Your password', type='password')

                st.markdown('###')
                login_submit_button = st.form_submit_button(label='Login')

                if login_submit_button:
                    authenticate_user_check = check_user_pass(username, password)

                    if authenticate_user_check == False:
                        st.error('Invalid Username or Password!')

                    else:
                        st.session_state['LOGGER_IN'] = True
                        self.cookies['__streamlit_login_signup_ui_username__'] = username
                        self.cookies.save()
                        del_login.empty()
                        st.experimental_rerun()

    def logout_widget(self) -> None:
        """登陆后创建退出部件"""
        if st.session_state['LOGGED_IN']:
            del_logout = st.sidebar.empty()
            del_logout.markdown('#')
            logout_click_check = del_logout.button(self.logout_button_name)

            if logout_click_check:
                st.session_state['LOGOUT_BUTTON_HIT'] = True
                st.session_state['LOGGED_IN'] = False
                self.cookies['__streamlit_login_signup_ui_username__'] = '8be4544f-a3d2-7e86-ca20-c914acac1bfa'
                del_logout.empty()
                st.experimental_rerun()

    def nav_sidebar(self):
        """创建侧边导航栏"""
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title='Navigation',
                menu_icon='list-columns-reverse',
                icons=['box-arrow-in-right', 'person-plus', 'x-circle', 'arrow-counterclockwise'],
                options=['Login', 'Create Account', 'Forgot Password?', 'Reset Password'],
                styles={
                    'container': {'padding': '5px'},
                    'nav-link': {'font-size': '14pz', 'text-algin': 'left', 'margin': '0px'}
                })
        return main_page_sidebar, selected_option

    def hide_menu(self) -> None:
        """隐藏菜单栏"""
        st.markdown(""" <style>#MainMenu {visibility:hidden;}</style> """, unsafe_allow_html=True)

    def hide_footer(self) -> None:
        """隐藏页脚"""
        st.markdown(""" <style>footer {visibility:hidden;}</style> """, unsafe_allow_html=True)

    def build_login_ui(self):
        """功能调用集合"""
        if 'LOGGED_IN' not in st.session_state:
            st.session_state['LOGGED_IN'] = False

        if 'LOGOUT_BUTTON_HIT' not in st.session_state:
            st.session_state['LOGOUT_BUTTON_HIT'] = False

        auth_json_exists_bool = self.check_auth_json_file_exists('_secret_auth_.json')

        if auth_json_exists_bool == False:
            with open('_secret_auth_.json', 'w') as auth_json:
                json.dump([], auth_json)

        main_page_sidebar, selected_option = self.nav_sidebar()

        if selected_option == 'Login':
            c1, c2 = st.columns([7, 3])
            with c1:
                self.login_widget()
            with c2:
                if st.session_state['LOGGED_IN'] == False:
                    self.animation()

        if selected_option == 'Create Account':
            self.sign_up_widget()

        if selected_option == 'Forgot Password?':
            self.forgot_password()

        if selected_option == 'Reset Password':
            self.reset_password()

        self.logout_widget()

        if st.session_state['LOGGED_IN'] == True:
            main_page_sidebar.empty()
