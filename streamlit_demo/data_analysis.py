# -*- coding: UTF-8 -*-
"""
csv excel文件分析工具
"""
import os
import copy

import streamlit as st
import pandas as pd
import plotly.express as px


def get_file_list(suffix, path):
    """
    获取当前目录所有指定后缀名的文件名列表、绝对路径列表
    :param suffix:
    :return:文件名列表、绝对路径列表
    """
    input_template_all = []
    input_template_all_path = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            if os.path.splitext(name)[1] == suffix:
                input_template_all.append(name)
                input_template_all_path.append(os.path.join(root, name))

    return input_template_all, input_template_all_path


st.title('数据分析工具')
input_folder = st.sidebar.text_input("输入数据所在的目录:(默认为脚本所在目录)，可输入新的路径回车更新",
                                     value=os.path.abspath('.'), key=None)
path = input_folder
# todo 待优化。拓展其它格式的数据
_, file_list_xlsx = get_file_list(".xlsx", path)
file_list = file_list_xlsx
# 如果目标文件存在
if file_list:
    select_file = st.sidebar.selectbox(
        '在当前目录下选择需要加载的文件:',
        file_list
    )
    st.write('You selected:', select_file)

    # 提取数据  st.cache_data的作用是当您使用 Streamlit 的缓存注释标记函数时，它会告诉 Streamlit 每当调用该函数时，它应该检查三件事：
    #
    # 函数名称
    # 构成函数体的实际代码
    # 调用函数的输入参数
    # 如果这是 Streamlit 第一次看到这三个项目，具有这些确切的值，并且在那个确切的组合中，它会运行该函数并将结果存储在本地缓存中。
    #
    # 然后，下次调用该函数时，如果这三个值没有更改，Streamlit 知道它可以完全跳过执行该函数。相反，它只是从本地缓存中读取输出并将其传递给调用者。
    @st.cache_data
    def load_data(path):
        df_ = pd.read_excel(path)
        df_.columns = df_.columns.str.lower()
        return df_
    df = load_data(select_file)
    col_list = df.columns
    # 将DF数据转为列表
    col_list = col_list.to_list()
    # 界面每次更新，此处亦会更新，为了保证数据的原始性，操作备份的数据
    col_list_bak = copy.deepcopy(col_list)
    # 渲染数据
    if len(col_list_bak) > 1:
        # 渲染数据
        sub_df = df[col_list_bak]
        sub_df = sub_df.drop(df.columns[[0]], axis=1)
        col_list_bak.pop(0)
        fig = px.line(sub_df, x=df['time'], y=col_list_bak, width=1080, height=550)
        fig.update_layout(legend=dict(
            orientation="h",  # 开启水平显示
        ))
        st.plotly_chart(fig, theme="streamlit")
else:
    st.title('没找到合适的文件，请检查')
