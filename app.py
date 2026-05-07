import streamlit as st
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="Agouti基因甲基化模拟", layout="centered", initial_sidebar_state="collapsed")

# --- 2. 核心设定：固定DNA序列 ---
DNA_TOP_SEQUENCE = "ATGCAGTCGATCGA"

def get_complement(base):
    """严格互补配对：A-T, C-G"""
    pairs = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return pairs.get(base, '')

DNA_BOTTOM_SEQUENCE = "".join([get_complement(b) for b in DNA_TOP_SEQUENCE])

# --- 3. 样式设置 ---
st.markdown("""
    <style>
    /* 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    body {
        background-color: #F7F9FA;
        font-family: 'Inter', sans-serif;
        color: #2C3E50;
    }
    /* 隐藏菜单 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* 标题样式 */
    h1, h2, h3 {font-weight: 600; color: #2C3E50;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    
    /* DNA 序列样式 */
    .dna-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 20px 0;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 18px;
        letter-spacing: 5px;
    }
    .dna-strand {
        display: flex;
        align-items: center;
    }
    .base {
        width: 30px;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        margin: 0 2px;
        color: white;
        position: relative;
        z-index: 2;
    }
    .base-A {background-color: #FF6B6B;} /* Red */
    .base-T {background-color: #4ECDC4;} /* Teal */
    .base-C {background-color: #FFD93D;} /* Yellow */
    .base-G {background-color: #1A535C;} /* Dark Blue */
    
    .connector {
        width: 2px;
        height: 20px;
        background-color: #E0E0E0;
        margin: 0 14px; /* Adjust based on base size */
        z-index: 1;
    }
    
    /* 甲基化标记 (CH3) */
    .methyl-group {
        position: absolute;
        top: -25px;
        font-size: 12px;
        color: #E74C3C;
        font-family: sans-serif;
        font-weight: bold;
        animation: float 2s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
        100% { transform: translateY(0px); }
    }

    /* 实验参数滑块样式 */
    .stSlider > div > div > div > div {
        background-color: #3498DB !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 侧边栏/头部信息 ---
st.markdown("<h2>🧪 实验参数</h2>", unsafe_allow_html=True)

# --- 5. 核心交互：甲基化滑块 ---
methylation_level = st.slider(
    "调节启动子甲基化水平", 
    min_value=0, 
    max_value=100, 
    value=0, 
    step=1,
    help="拖动滑块模拟环境因素对Agouti基因启动子区域甲基化程度的影响"
)

# --- 6. 分子结构观察 (保持原有逻辑) ---
st.markdown("<h3>🔬 分子结构观察</h3>", unsafe_allow_html=True)

# 计算需要显示的CH3数量 (假设序列长度为14，最多显示14个)
num_bases = len(DNA_TOP_SEQUENCE)
# 根据百分比计算显示多少个CH3，至少显示1个如果大于0
num_ch3 = int((methylation_level / 100) * num_bases)

col1, col2 = st.columns([2, 1])

with col1:
    # 构建DNA HTML
    dna_html = '<div class="dna-container"><div class="dna-strand">'
    
    # 上链 (带CH3)
    for i in range(num_bases):
        base = DNA_TOP_SEQUENCE[i]
        # 检查当前位置是否需要显示CH3
        ch3_tag = f'<div class="methyl-group">CH3</div>' if i < num_ch3 else ''
        dna_html += f'<div class="base base-{base}">{ch3_tag}{base}</div>'
    
    dna_html += '</div><div class="dna-strand">'
    
    # 连接线
    for _ in range(num_bases):
        dna_html += '<div class="connector"></div>'
        
    dna_html += '</div><div class="dna-strand">'
    
    # 下链
    for base in DNA_BOTTOM_SEQUENCE:
        dna_html += f'<div class="base base-{base}">{base}</div>'
        
    dna_html += '</div></div>'
    
    st.markdown(dna_html, unsafe_allow_html=True)
    st.caption("注：红色 CH3 代表甲基化修饰。启动子区域甲基化程度越高，基因表达越受抑制。")

# --- 7. 表型观察 (重点修改部分) ---
st.markdown("---")
st.markdown("<h3>🐭 表型观察</h3>", unsafe_allow_html=True)

# 根据滑块数值决定显示哪只小鼠
# 逻辑：低甲基化 -> 黄色; 中等 -> 灰色; 高甲基化 -> 黑色
if methylation_level < 33:
    # 低甲基化：黄色
    mouse_img = "yellow.png"
    status_text = "黄色 (活跃)"
    status_color = "#D4AC0D"
    conclusion_text = """
    - **状态**：启动子低甲基化。
    - **机制**：转录因子顺利结合，Agouti基因持续高表达。
    - **结果**：小鼠毛色呈现**黄色**，且易肥胖、易患糖尿病。
    """
elif methylation_level < 66:
    # 中等甲基化：灰色 (中间态)
    mouse_img = "gray.png"  # 修正了文件名拼写
    status_text = "灰色 (部分抑制)"
    status_color = "#7F8C8D"
    conclusion_text = """
    - **状态**：启动子中等甲基化。
    - **机制**：部分基因表达被抑制。
    - **结果**：小鼠毛色呈现**灰色**（杂色/中间色）。
    """
else:
    # 高甲基化：黑色
    mouse_img = "black.png"
    status_text = "黑色 (沉默)"
    status_color = "#2C3E50"
    conclusion_text = """
    - **状态**：启动子高甲基化。
    - **机制**：甲基基团阻碍转录因子结合，Agouti基因表达被抑制。
    - **结果**：小鼠毛色呈现**黑色**，体型正常，健康。
    """

# 显示图片和结论
col_mouse, col_conclusion = st.columns([1, 1])

with col_mouse:
    st.markdown("**小鼠毛色**")
    # --- 关键修改点：使用 unsafe_allow_html=True 来渲染图片 ---
    # 注意：确保 yellow.png, gray.png, black.png 与代码在同一目录下
    st.markdown(
        f'< img src="{mouse_img}" style="width:100%; border-radius:10px; border: 2px solid {status_color}; margin-top:10px;">', 
        unsafe_allow_html=True
    )
    st.markdown(f"表型状态：**<span style='color:{status_color}'>{status_text}</span>**", unsafe_allow_html=True)

with col_conclusion:
    st.markdown("**实验结论**")
    st.markdown(conclusion_text)
