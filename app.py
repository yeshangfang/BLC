import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 设置页面布局
st.set_page_config(layout="wide")

# 定义函数计算光合作用强度
def calculate_photosynthesis_intensity(light_quality, co2_concentration, light_intensity):
    # 这里我们假设一个简单的模型：光合作用强度 = 光质 * CO2浓度 * 光照强度
    photosynthesis_intensity = light_quality * co2_concentration * light_intensity / 1000.0
    return photosynthesis_intensity

# 定义函数生成气泡数量
def generate_bubble_count(photosynthesis_intensity):
    bubble_count = max(0,int(photosynthesis_intensity * 5)  # 假设每单位光合强度产生5个气泡
    return bubble_count

# 左侧部分：自变量设置
st.sidebar.header("实验条件设置")
light_quality = st.sidebar.slider("光质 (nm)", min_value=400, max_value=700, value=680)
co2_concentration = st.sidebar.slider("CO2 浓度 (ppm)", min_value=300, max_value=1500, value=400)
light_intensity = st.sidebar.slider("光照强度 (μmol/m²/s)", min_value=100, max_value=2000, value=1000)

# 计算光合作用强度
photosynthesis_intensity = calculate_photosynthesis_intensity(light_quality, co2_concentration, light_intensity)

# 右侧部分：因变量呈现
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("当前光合作用强度")
    st.write(f"**{photosynthesis_intensity:.2f} μmol O₂/(g h)**")

    st.subheader("烧杯中气泡数量模拟")
    bubble_count = generate_bubble_count(photosynthesis_intensity)
    bubble_svg = f"""
    <svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <rect x="0" y="0" width="200" height="200" fill="#add8e6"/>
        {''.join(f'<circle cx="{np.random.randint(10, 190)}" cy="{np.random.randint(10, 190-bubble*10)}" r="5" fill="#FFD700"/>' for bubble in range(bubble_count))}
    </svg>
    """
    st.markdown(bubble_svg, unsafe_allow_html=True)

with col2:
    st.subheader("光合作用强度变化曲线图")
    # 模拟一段时间内的光合作用强度变化
    time_points = np.linspace(0, 10, num=100)  # 时间点从0到10小时
    intensity_values = [calculate_photosynthesis_intensity(light_quality, co2_concentration, li) for li in np.linspace(100, light_intensity, num=100)]

    fig, ax = plt.subplots()
    ax.plot(time_points, intensity_values, label='光合作用强度')
    ax.set_xlabel('时间 (小时)')
    ax.set_ylabel('光合作用强度 (μmol O₂/(g h))')
    ax.legend()
    st.pyplot(fig)

# 结论部分
st.header("实验结论")
conclusion_text = (
    f"根据设定的实验条件（光质: {light_quality} nm, "
    f"CO2 浓度: {co2_concentration} ppm, 光照强度: {light_intensity} μmol/m²/s），"
    f"计算得到的光合作用强度为 **{photosynthesis_intensity:.2f} μmol O₂/(g h)**。\n\n"
    f"在烧杯中模拟产生了约 **{bubble_count}** 个气泡，这表明植物在当前条件下进行着活跃的光合作用过程。\n\n"
    "您可以继续调整实验条件以观察其对光合作用强度的影响。"
)
st.write(conclusion_text)
