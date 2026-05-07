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

    /* DNA 结构样式 */
    .dna-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 20px 0;
        padding: 20px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }}

    .dna-strand {{
        display: flex;
        justify-content: space-between;
        width: 100%;
        padding: 0 20px;
        position: relative;
        z-index: 2;
    }}

    .base {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 18px;
        color: #333;
        position: relative;
        z-index: 3;
    }}

    .top-base {{ background-color: #FFD1DC; border: 2px solid #FF69B4; }} /* 粉色 */
    .bottom-base {{ background-color: #ADD8E6; border: 2px solid #1E90FF; }} /* 蓝色 */

    .connector {{
        height: 20px;
        border-left: 2px dashed #ccc;
        margin: 0 10px;
        position: relative;
        top: 10px;
    }}

    /* 甲基化标记 (CH3) */
    .methyl-group {{
        position: absolute;
        top: -35px; /* 位于碱基上方 */
        font-size: 12px;
        font-weight: bold;
        color: #D32F2F;
        background: rgba(255, 255, 255, 0.8);
        padding: 2px 4px;
        border-radius: 4px;
        border: 1px solid #D32F2F;
        animation: float 2s infinite ease-in-out;
    }}

    @keyframes float {{
        0% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-5px); }}
        100% {{ transform: translateY(0px); }}
    }}

    /* 结果区域 */
    .result-container {{
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        gap: 20px;
        margin-top: 30px;
    }}

    .card {{
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        flex: 1;
        min-width: 300px;
        text-align: center;
    }}

    .mouse-wrapper {{
        position: relative;
        display: inline-block;
        margin-top: 15px;
    }}

    /* 关键修复：确保图片显示并应用滤镜 */
    .mouse-img {{
        width: 200px;
        height: auto;
        border-radius: 10px;
        display: block;
    }}

    /* 动态颜色层 */
    .color-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 200px;
        height: 100%;
        border-radius: 10px;
        pointer-events: none;
        /* 颜色混合模式，让黑色叠在黄色上变成褐色/黑色 */
        mix-blend-mode: multiply;
        background-color: rgba(0, 0, 0, {methylation_level / 100});
        transition: background-color 0.3s ease;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. 构建 DNA 可视化 ---
def build_dna_visualization(methylation):
    html = '<div class="dna-container"><div class="dna-strand">'

    # 上链
    for i, base in enumerate(DNA_TOP_SEQUENCE):
        # 计算该碱基是否需要显示甲基化 (前 7 个碱基为启动子区域)
        show_methyl = " "
        # 简单的概率逻辑：如果随机数小于甲基化水平，则显示
        if i < 7 and random.randint(0, 100) < methylation:
            show_methyl = '<div class="methyl-group">CH3</div>'

        html += f"""
        <div style="position: relative; display: flex; flex-direction: column; align-items: center;">
            {show_methyl}
            <div class="base top-base">{base}</div>
        </div>
        """
    html += '</div>'  # End Top Strand

    # 连接线
    html += '<div style="display: flex; justify-content: space-between; width: 100%; padding: 0 20px;">'
    for _ in DNA_TOP_SEQUENCE:
        html += '<div class="connector"></div>'
    html += '</div>'

    # 下链
    html += '<div class="dna-strand">'
    for base in DNA_BOTTOM_SEQUENCE:
        html += f'<div class="base bottom-base">{base}</div>'
    html += '</div></div>'  # End Bottom Strand & Container

    return html

# --- 6. 页面主体布局 ---
st.markdown("<h2 style='text-align: center;'>✒️ Agouti 基因甲基化模拟</h2>", unsafe_allow_html=True)

# 显示 DNA 结构 (每次重绘会重新计算甲基化分布，模拟随机性)
st.markdown(build_dna_visualization(methylation_level), unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #666; font-size: 12px;'>注：CH3 代表甲基化基团，启动子区域甲基化程度越高，基因表达受抑制越强。</p >", unsafe_allow_html=True)

# --- 7. 结果展示区域 ---
st.markdown('<div class="result-container">', unsafe_allow_html=True)

# 左侧：表型观察
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🐭 表型观察")

    # 根据甲基化水平确定文字描述
    if methylation_level < 30:
        status_text = "基因**高度表达**\n\n小鼠呈现**黄色**，且通常体型肥胖。"
        status_color = "orange"
    elif methylation_level > 70:
        status_text = "基因**受到抑制**\n\n小鼠呈现**黑色** (或伪黑色)，体型正常。"
        status_color = "black"
    else:
        status_text = "基因**部分表达**\n\n小鼠呈现**介于黄黑之间的过渡色** (褐色/杂色)。"
        status_color = "brown"

    # 图片显示逻辑 (使用 try-except 防止报错)
    try:
        # 确保文件名正确
        st.markdown(f"""
        <div class="mouse-wrapper">
            < img src="yellow.png" class="mouse-img" alt="Mouse">
            <div class="color-overlay"></div>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error("图片加载失败，请确保 yellow.png 在同一目录下")

    st.markdown('</div>', unsafe_allow_html=True) # Close card

# 右侧：实验结论
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 实验结论")

    st.markdown(f"""
    #### 当前状态
    - **甲基化水平**: {methylation_level}%
    - **毛色表现**: <span style='color:{status_color}; font-weight:bold;'>{status_text.split('**')[1]}</span>

    #### 原理分析
    1. **低甲基化 (<30%)**: 启动子未被修饰，转录因子可结合，Agouti 基因持续表达，小鼠为黄色。
    2. **高甲基化 (>70%)**: 启动子区域结合了大量甲基基团，阻碍转录，Agouti 基因沉默，小鼠恢复为黑色 (野生型)。
    3. **表观遗传**: DNA 序列 (`ATGC...`) 始终**未发生改变**，但基因表达发生了可遗传的变化。
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True) # Close card

st.markdown('</div>', unsafe_allow_html=True) # Close result container
