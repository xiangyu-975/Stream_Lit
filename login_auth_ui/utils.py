#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/29 16:39
@Author  : Nick
@File    : utils.py
@Software: PyCharm
"""
import json
import logging
import re
import secrets

import requests
from argon2 import PasswordHasher
from trycourier import Courier

ph = PasswordHasher()
logger = logging.getLogger(__name__)


def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """检查当前密码"""
    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_reset_passwd:
                try:
                    if ph.verify(user['password'], current_passwd):
                        return True
                except Exception as e:
                    logger.error(e)
    return False


def check_email_exists(email_forgot_password: str):
    """检查邮箱是否存在"""
    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_forgot_password:
                return True, user['email']
    return False, None


def send_passwd_in_email(auth_token: str, username_forget_passwd: str, email_forgot_passwd: str, company_name: str,
                         random_passwd: str) -> None:
    """发送验证码"""
    client = Courier(auth_token=auth_token)

    resp = client.send_message(
        message={
            'to': {
                'email': email_forgot_passwd,
            },
            'content': {
                'title': company_name + ': Login PassWord!',
                'body': 'Hi! ' + username_forget_passwd + ',' + '\n' + '\n' + 'Your temporary login passwd is: ' + random_passwd + '\n' + '\n' + '{{info}}',
            },
            'data': {
                'info': 'Please reset your password at the earliest for security reasons.'
            }
        })


def change_passwd(email_: str, random_passwd: str) -> None:
    """更新密码"""
    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)
    with open('_secret_auth_.json', 'w') as auth_json:
        for user in authorized_users_data:
            if user['email'] == email_:
                user['passwd'] = ph.hash(random_passwd)
        json.dump(authorized_users_data, auth_json)


def generate_random_passwd() -> str:
    """验证码生成"""
    password_length = 10
    return secrets.token_urlsafe(password_length)


def register_new_user(name_sign_up: str, email_sign_up: str, password_sign_up: str, username_sign_up: str) -> None:
    """注册新用户,新用户信息存入Json文件"""
    new_user_data: dict = {
        'username': username_sign_up,
        'name': name_sign_up,
        'email': email_sign_up,
        'password': ph.hash(password_sign_up)
    }

    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_user_data = json.load(auth_json)

    with open('_secret_auth_.json', 'w') as auth_json_write:
        authorized_user_data.append(new_user_data)
        json.dump(authorized_user_data, auth_json_write)


def non_empty_str_check(username_sign_up: str) -> bool:
    """检查字符串是否为空"""
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count += 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_user(username_sign_up: str) -> bool:
    """检查用户是否唯一"""
    authorized_user_data_master = list()
    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])

    if username_sign_up in authorized_user_data_master:
        return False

    no_empty_check = non_empty_str_check(username_sign_up)

    if not no_empty_check:
        return None
    return True


def check_unique_email(email_sign_up: str) -> bool:
    """检查邮箱是否唯一"""
    authorized_user_data_master = list()
    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['email'])

    if email_sign_up in authorized_user_data_master:
        return False
    return True


def check_valid_email(email_sign_up: str) -> bool:
    """检查邮箱是否合法"""
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(email_regex, email_sign_up):
        return True
    return False


def check_valid_name(name_sign_up: str) -> bool:
    """检查用户名是否合法"""
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')
    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_user_pass(username: str, password: str) -> bool:
    """验证用户信息"""
    with open('_secret_auth_.json', 'r') as auth_json:
        authorized_user_data = json.load(auth_json)

    for registered_user in authorized_user_data:
        if registered_user['username'] == username:
            try:
                passwd_verification_bool = ph.verify(registered_user['password'], password)
                if passwd_verification_bool:
                    return True
            except Exception as e:
                logger.info(e)
    return False


def load_lottieurl(url: str) -> str:
    """使用url获取lottie动画"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    url = "https://assets8.lottiefiles.com/packages/lf20_ktwnwv5m.json"
    load_lottieurl(url)
