import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 设置页面标题
st.title("🌿 光合作用强度模拟器")

# 侧边栏设置
st.sidebar.header("参数设置")
light_quality = st.sidebar.slider("光质 (波长 nm)", 400, 700, 680)
co2_concentration = st.sidebar.slider("二氧化碳浓度 (ppm)", 300, 1500, 400)
light_intensity = st.sidebar.slider("光照强度", 100, 2000, 1000)

# 计算函数
def calculate_photosynthesis(lq, co2, li):
    return (lq * co2 * li) / 1000000

# 计算结果
result = calculate_photosynthesis(light_quality, co2_concentration, light_intensity)
st.write(f"当前光合作用强度: **{result:.2f}**")

# 绘图
fig, ax = plt.subplots()
ax.bar(["当前强度"], [result], color='green')
ax.set_ylabel("强度值")
st.pyplot(fig)
