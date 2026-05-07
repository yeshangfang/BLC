import streamlit as st

# --- 1. 页面配置 ---
st.set_page_config(page_title="Agouti基因甲基化模拟", layout="centered", initial_sidebar_state="collapsed")

# --- 2. 核心设定：固定DNA序列 ---
# 固定上链序列（14个碱基），完全符合教材标准
DNA_TOP_SEQUENCE = "ATGCAGTCGATCGA"

def get_complement(base):
    """严格互补配对：A-T, C-G"""
    pairs = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return pairs.get(base, '')

# 自动生成严格互补的下链序列
DNA_BOTTOM_SEQUENCE = "".join([get_complement(b) for b in DNA_TOP_SEQUENCE])

# --- 3. 侧边栏：甲基化调节 ---
with st.sidebar:
    st.header("🧬 实验控制")
    methylation_level = st.slider(
        "调节甲基化水平",
        min_value=0,
        max_value=100,
        value=10,
        step=1,
        help="拖动滑块改变甲基化程度"
    )
    st.info(f"当前设定：**{methylation_level}%**")

# --- 4. 样式设置 ---
st.markdown(f"""
    <style>
    /* 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    body {{
        background-color: #F7F9FA;
        font-family: 'Inter', sans-serif;
    }}

    /* DNA 容器样式 */
    .dna-container {{
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 30px;
        border: 1px solid #E0E0E0;
    }}

    /* DNA 单链样式 */
    .dna-strand {{
        display: flex;
        justify-content: center;
        gap: 12px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 18px;
        color: #333;
    }}

    /* 碱基盒子 */
    .base-box {{
        width: 40px;
        height: 40px;
        background-color: #E3F2FD;
        border: 1px solid #90CAF9;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        transition: all 0.3s ease;
    }}

    /* 甲基化标记样式（替换红点为CH3） */
    .methyl-mark {{
        position: absolute;
        top: -28px; /* 调整位置，使其在碱基上方 */
        font-size: 14px;
        font-weight: bold;
        color: #D32F2F;
        font-family: 'Courier New', monospace;
        opacity: 0;
        transform: translateY(5px);
        transition: all 0.3s ease;
        background: white;
        padding: 2px 4px;
        border-radius: 4px;
        border: 1px solid #D32F2F;
    }}

    /* 连接线 */
    .connector {{
        width: 2px;
        height: 20px;
        background-color: #B0BEC5;
        margin: 0 19px; /* 调整连接线位置 */
    }}

    /* 小鼠图片容器 */
    .mouse-container {{
        position: relative;
        width: 300px;
        height: 300px;
        margin: 0 auto;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        background-color: white;
    }}

    /* 小鼠图片 */
    .mouse-img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        transition: filter 0.5s ease;
    }}

    /* 黑色遮罩层 */
    .mouse-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: black;
        opacity: 0;
        transition: opacity 0.5s ease;
        pointer-events: none;
    }}

    /* 实验结论卡片 */
    .conclusion-card {{
        background: #E8F5E9;
        border-left: 5px solid #4CAF50;
        padding: 20px;
        border-radius: 10px;
        margin-top: 30px;
        font-size: 16px;
        line-height: 1.6;
        color: #2E7D32;
    }}

    /* 标题样式 */
    h1 {{
        color: #1565C0;
        text-align: center;
        font-weight: 600;
        margin-bottom: 30px;
        font-family: 'Inter', sans-serif;
    }}

    /* 响应式调整 */
    @media (max-width: 600px) {{
        .base-box {{
            width: 30px;
            height: 30px;
            font-size: 14px;
        }}
        .methyl-mark {{
            font-size: 12px;
            top: -24px;
        }}
        .connector {{
            height: 15px;
            margin: 0 14px;
        }}
        .mouse-container {{
            width: 250px;
            height: 250px;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. 页面主体 ---
st.markdown("<h1>🧬 Agouti 基因甲基化模拟</h1>", unsafe_allow_html=True)

# --- 6. DNA 结构可视化 ---
st.markdown('<div class="dna-container">', unsafe_allow_html=True)

# 上链
st.markdown('<div class="dna-strand">', unsafe_allow_html=True)
for i, base in enumerate(DNA_TOP_SEQUENCE):
    # 计算当前碱基是否甲基化（根据滑块百分比）
    # 这里为了演示，我们固定某些位置为甲基化，或者随机
    # 为了让效果更明显，我们根据滑块值决定显示多少个CH3
    num_methylated = int(len(DNA_TOP_SEQUENCE) * (methylation_level / 100))
    # 随机选择甲基化位置（为了稳定性，使用seed）
    random.seed(42)  # 固定随机种子，保证每次刷新位置不变
    methylated_indices = random.sample(range(len(DNA_TOP_SEQUENCE)), num_methylated)

    is_methylated = i in methylated_indices

    methyl_html = '<span class="methyl-mark" style="opacity: 1;">CH₃</span>' if is_methylated else ""

    st.markdown(f"""
        <div class="base-box">
            {base}
            {methyl_html}
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 连接线
st.markdown('<div class="dna-strand">', unsafe_allow_html=True)
for _ in DNA_TOP_SEQUENCE:
    st.markdown('<div class="connector"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 下链
st.markdown('<div class="dna-strand">', unsafe_allow_html=True)
for base in DNA_BOTTOM_SEQUENCE:
    st.markdown(f"""
        <div class="base-box">
            {base}
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # End dna-container

# --- 7. 小鼠表型展示 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🐭 表型观察")
    # 计算遮罩透明度：甲基化越高，遮罩越不透明（小鼠越黑）
    # 0% 甲基化 -> 0.0 透明度 (黄色)
    # 100% 甲基化 -> 0.9 透明度 (黑色)
    overlay_opacity = methylation_level / 100 * 0.9

    # 使用HTML和CSS来实现图片变色
    mouse_html = f"""
    <div class="mouse-container">
        < img src="https://i.imgur.com/8Z4z4zL.png" class="mouse-img"> <!-- 黄色小鼠图片 -->
        <div class="mouse-overlay" style="opacity: {overlay_opacity};"></div>
    </div>
    """
    st.markdown(mouse_html, unsafe_allow_html=True)

    # 显示当前颜色状态
    color_status = "黄色 (肥胖)" if methylation_level < 30 else "褐色 (中间型)" if methylation_level < 70 else "黑色 (苗条)"
    st.caption(f"当前毛色状态：**{color_status}**")

with col2:
    st.subheader("📝 实验结论")
    # 动态生成结论
    if methylation_level < 30:
        conclusion = """
        - **基因表达**：Agouti 基因**高度表达**。
        - **表型结果**：小鼠毛色呈**黄色**，且容易肥胖，易患糖尿病。
        - **机制**：启动子区域低甲基化，RNA聚合酶易于结合。
        """
    elif methylation_level < 70:
        conclusion = """
        - **基因表达**：Agouti 基因**部分表达**。
        - **表型结果**：小鼠毛色呈**褐色/伪黄色**。
        - **机制**：启动子区域部分甲基化，基因表达受到一定抑制。
        """
    else:
        conclusion = """
        - **基因表达**：Agouti 基因**被沉默（不表达）**。
        - **表型结果**：小鼠毛色呈**黑色**，体型苗条健康。
        - **机制**：启动子区域高甲基化，阻碍了转录因子的结合。
        """

    st.markdown(f"""
    <div class="conclusion-card">
        <strong>当前甲基化水平：{methylation_level}%</strong>
        <ul style="margin-top: 10px; padding-left: 20px;">
            {"".join([f"<li>{item.strip()}</li>" for item in conclusion.split('\n') if item.strip()])}
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- 8. 底部说明 ---
st.markdown("---")
st.markdown("""
<center>
    <small>
    **教学说明**：本模拟展示了表观遗传学中的DNA甲基化现象。
    即使基因序列（DNA）不变，化学修饰（如甲基化）也能显著改变生物的性状。
    </small>
</center>
""", unsafe_allow_html=True)
