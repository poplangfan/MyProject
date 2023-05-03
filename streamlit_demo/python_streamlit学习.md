# Streamlit学习  

基于`python3.8`和`streamlit 1.21.0`。   

### 学习新框架的一点小技巧

- 不要看太多教程，1~2个为佳，快速掌握基本语法后，多实践；

  > [https://streamlit.io](https://streamlit.io/)
  >
  >[Streamlit开发手册 - 汇智网 (hubwiz.com)](http://cw.hubwiz.com/card/c/streamlit-manual/)

### 优点

- 用于机器学习、数据可视化的 Python 框架，它能几行代码就构建出一个精美的在线 app 应用；
- Streamlit 在几分钟内将数据脚本转换为可共享的 Web 应用程序；
- 一切都是纯Python实现，无需前端经验;
- 学习成本极低。


## 总体计划

- 总体介绍
- 官网示例讲解
- 自己实现一个功能
- 优秀的案例分析讲解

### day01--20230411

- 总体介绍

安装方式：`pip install streamlit`

运行方式：`streamlit run xx.py`

示例demo:

```
import streamlit as st
import pandas as pd

st.write("""
# My first app
Hello *world!*""")

df = pd.read_csv("my_data.csv")
st.line_chart(df)

```



### day02--20230411

- 官网示例讲解

plotly介绍 ：[一文爱上高级可视化神器Plotly - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/370656578)

plotly的安装：`pip install plotly`

demo1:

```
import streamlit as st
import numpy as np
import plotly.figure_factory as ff

# Add histogram data
x1 = np.random.randn(200) - 2
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3']

# Create distplot with custom bin_size
fig = ff.create_distplot(
        hist_data, group_labels, bin_size=[.1, .25, .5])

# Plot!
st.plotly_chart(fig, use_container_width=True)
```



demo2:

```
import plotly.express as px
import streamlit as st

df = px.data.gapminder()

fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    # Use the Streamlit theme.
    # This is the default. So you can also omit the theme argument.
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    # Use the native Plotly theme.
    st.plotly_chart(fig, theme=None, use_container_width=True)

```



### day03-20230503

- 自己实现一个功能

```python
# -*- coding: UTF-8 -*-
"""
csv excel文件分析工具
"""
import copy
import os
import plotly.express as px

import pandas as pd
import streamlit as st

# 默认打开默认wide mode
st.set_page_config(layout="wide")


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
# # 选择其它目录， 暂时没找到方法，用输入路径代替
input_folder = st.sidebar.text_input("输入数据所在的目录:(默认为脚本所在目录)，可输入新的路径回车更新",
                                     value=os.path.abspath('.'), key=None)
# 获取目录下所有csv文件
path = input_folder
_, file_list_xlsx = get_file_list(".xlsx", path)
_, file_list_csv = get_file_list(".csv", path)
file_list_csv.extend(file_list_xlsx)
file_list = file_list_csv
# 如果目标文件存在
if file_list:
    # 左侧下拉选择要分析的文件，默认目录)
    select_file = st.sidebar.selectbox(
        '在当前目录下选择需要加载的文件:',
        file_list)
    st.write('You selected:', select_file)
    # 两个按钮横向排列, 此方法不行，暂时不用
    # col1, col2 = st.sidebar.columns([1, 1])
    # with col1:
    #     select_value_all = st.button("select all")
    # with col2:
    #     genre = st.button("select no")
    genre = st.sidebar.radio(
        "select all or select no",
        ('select all', 'select no'))

    # 获取选择csv所有的列名（默认第一列为时间戳，不加载）
    @st.cache_data
    def load_data(path):
        if ".csv" in path:
            try:
                df_ = pd.read_csv(path)
            except:
                st.write("csv格式异常")
        else:
            df_ = pd.read_excel(path)
        df_.columns = df_.columns.str.lower()
        return df_


    df = load_data(select_file)
    col_list = df.columns
    # 将DF数据转为列表
    col_list = col_list.to_list()
    if col_list[0] == "time":
        # 求取每列的最大值、最小值
        for i in range(1, len(col_list)):
            col_list[i] = col_list[i] + "   " + str(f"【{'%.2f'%list(df.min())[i]}, {'%.2f'%list(df.max())[i]}】")
        # 列名重命名
        df.columns = col_list
        # 界面每次更新，此处亦会更新，为了保证数据的原始性，操作备份的数据
        col_list_bak = copy.deepcopy(col_list)
        # 删除时间列
        # df = df.drop(df.columns[[0]], axis=1)
        # col_list = df.columns
        # 显示可以选择的列
        # 此处逻辑需要完善：1、默认应该是全选的 2、重新选择后，结果应该重新刷新
        for index, select in enumerate(col_list):
            if select == 'time':
                pass
            else:
                # done 1、默认应该是全选的
                if genre == "select no":
                    option = st.sidebar.checkbox(
                        select,
                        value=False
                    )
                    if option:
                        # done 2、重新选择后，结果应该重新刷新
                        pass
                    else:
                        col_list_bak.remove(select)
                else:
                    option = st.sidebar.checkbox(
                        select,
                        value=True
                    )
                    if option:
                        # done 2、重新选择后，结果应该重新刷新
                        pass
                    else:
                        col_list_bak.remove(select)
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
        st.title('目标文件不符合格式要求，请检查')
else:
    st.title('没找到合适的文件，请检查')
```

