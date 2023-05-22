#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/15 17:54
@Author  : Nick
@File    : myfile.py.py
@Software: PyCharm
"""
import numpy as np
import pandas as pd
import streamlit as st

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(chart_data)

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})
st.line_chart(df)
