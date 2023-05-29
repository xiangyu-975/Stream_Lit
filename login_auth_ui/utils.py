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

import requests
from argon2 import PasswordHasher

ph = PasswordHasher()
logger = logging.getLogger(__name__)


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
    with open('../_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])

    if username_sign_up in authorized_user_data_master:
        return False

    no_empty_check = non_empty_str_check(username_sign_up)

    if no_empty_check == False:
        return None
    return True


def check_unique_email(emial_sign_up: str) -> bool:
    """检查邮箱是否唯一"""
    authorized_user_data_master = list()
    with open('../_secret_auth_.json', 'r') as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['email'])

    if emial_sign_up in authorized_user_data_master:
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
    with open('../_secret_auth_.json', 'r') as auth_json:
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
