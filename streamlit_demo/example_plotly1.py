import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import scipy

# Add histogram data 添加直方图数据
x1 = np.random.randn(200) - 2  # 200个随机数据
x2 = np.random.randn(200)
x3 = np.random.randn(200) + 2

# Group data together
hist_data = [x1, x2, x3]

group_labels = ['Group 1', 'Group 2', 'Group 3'] # 添加标签

# Create distplot with custom bin_size
fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .1])

# Plot!
st.plotly_chart(fig, use_container_width=True)