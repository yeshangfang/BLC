import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义光合作用速率函数
def photosynthesis_rate(light_intensity, co2_concentration, light_quality):
    # 简化的光合作用速率方程
    return 0.1 * light_intensity * co2_concentration * (light_quality / 10)

# 模拟微分方程
def bubble_production(bubbles, t, light_intensity, co2_concentration, light_quality):
    rate = photosynthesis_rate(light_intensity, co2_concentration, light_quality)
    dbdt = rate - bubbles * 0.05  # 假设一部分气泡会消失
    return dbdt

# Streamlit应用
st.title("光合作用强度模拟器")

# 设置参数
light_intensity = st.slider("光照强度", min_value=0, max_value=100, value=50, step=1)
co2_concentration = st.slider("二氧化碳浓度 (ppm)", min_value=0, max_value=1000, value=400, step=10)
light_quality = st.selectbox("光质", options=["红光", "蓝光", "白光"], index=2)

# 将光质转换为数值
light_quality_values = {"红光": 700, "蓝光": 450, "白光": 550}
light_quality_num = light_quality_values[light_quality]

# 时间数组
t = np.linspace(0, 100, 100)

# 解微分方程
bubbles = odeint(bubble_production, y0=0, t=t, args=(light_intensity, co2_concentration, light_quality_num)).flatten()

# 计算光合作用强度
photosynthesis_strengths = [photosynthesis_rate(light_intensity, co2_concentration, light_quality_num) for _ in t]

# 绘制动态曲线图
fig, ax1 = plt.subplots(figsize=(10, 6))

color = 'tab:red'
ax1.set_xlabel('时间')
ax1.set_ylabel('光合作用强度', color=color)
ax1.plot(t, photosynthesis_strengths, color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('气泡数量', color=color)  
ax2.plot(t, bubbles, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()
st.pyplot(fig)

# 结论部分
st.subheader("结论")
conclusion = f"""
- **光照强度**: 当光照强度增加时，光合作用强度也增加，因为更多的能量用于驱动光反应。
- **二氧化碳浓度**: 随着二氧化碳浓度的提高，光合作用强度也会增加，直到达到饱和点。
- **光质**: 不同颜色的光影响光合色素吸收光的能量效率。在这个模型中，{light_quality}提供了最适合植物生长的能量范围。
"""

st.markdown(conclusion)
