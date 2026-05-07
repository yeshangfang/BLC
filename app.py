import streamlit as st

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

    /* 实验参数区 */
    .experiment-section {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 25px;
        border-left: 5px solid #3498DB;
    }

    /* DNA 结构样式 */
    .dna-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        font-size: 1.2rem;
        margin-top: 15px;
        background: #E8F4FD;
        padding: 15px;
        border-radius: 8px;
        position: relative;
    }
    .dna-strand {
        letter-spacing: 8px;
        display: flex;
        align-items: center;
    }
    .base {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 30px;
    }
    .bond {
        height: 10px;
        border-left: 2px solid #95A5A6;
        margin: 2px 0;
    }
    .methyl-tag {
        background-color: #E74C3C;
        color: white;
        font-size: 0.7rem;
        padding: 2px 5px;
        border-radius: 4px;
        margin-top: 5px;
        animation: popIn 0.5s ease;
    }
    @keyframes popIn {
        0% {transform: scale(0);}
        80% {transform: scale(1.2);}
        100% {transform: scale(1);}
    }

    /* 表型观察区 */
    .phenotype-section {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .mouse-image-container {
        margin: 20px auto;
        height: 250px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .conclusion-box {
        background-color: #F8F9FA;
        border-left: 4px solid #34495E;
        padding: 15px;
        margin-top: 20px;
        text-align: left;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 侧边栏控制 ---
with st.sidebar:
    st.header("⚙️ 实验参数调节")
    st.markdown("*拖动滑块改变甲基化程度*")
    methylation_level = st.slider(
        "甲基化水平 (Methylation Level)",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )

# --- 5. 主界面逻辑 ---

# 实验参数区
st.markdown('<div class="experiment-section"><h3>🧪 实验参数</h3></div>', unsafe_allow_html=True)

# 分子结构观察区
st.markdown("### 🧬 分子结构观察")

# 计算当前需要显示的甲基化数量 (0-14个位点)
num_methylated = int((methylation_level / 100) * 14)

# 构建DNA可视化
top_html = '<div class="dna-strand">'
bottom_html = '<div class="dna-strand">'

for i, base in enumerate(DNA_TOP_SEQUENCE):
    comp_base = DNA_BOTTOM_SEQUENCE[i]

    # 顶部链
    top_html += '<div class="base">'
    top_html += f'<span>{base}</span>'

    # 如果是C，且索引小于当前的甲基化数量，显示甲基基团
    # (为了演示效果，我们假设前N个C被甲基化)
    is_cytosine = (base == 'C')
    # 简单的逻辑：按顺序甲基化
    # 这里为了演示，我们假设前 num_methylated 个胞嘧啶被标记
    # 实际序列中C的位置：1, 5, 10, 13 (索引 1, 5, 10, 13)
    # 为了简单，我们直接按滑块数值控制显示几个标签
    c_positions = [1, 5, 10, 13] # C在序列中的索引
    show_methyl = False

    if is_cytosine and i in c_positions:
         # 计算这是第几个C
         c_index = c_positions.index(i)
         if c_index < num_methylated:
             show_methyl = True

    if show_methyl:
        top_html += '<div class="methyl-tag">CH3</div>'
    else:
        top_html += '<div style="height:22px;"></div>' # 占位符保持对齐

    top_html += '</div>'

    # 底部链 (互补链，通常CpG位点是回文的，这里简化处理)
    bottom_html += '<div class="base">'
    bottom_html += f'<span>{comp_base}</span>'
    bottom_html += '</div>'

top_html += '</div>'
bottom_html += '</div>'

# 显示DNA
st.markdown(f"""
<div class="dna-container">
    <div style="font-size:0.8rem; color:#7F8C8D; margin-bottom:5px;">启动子区域 (Promoter)</div>
    {top_html}
    <div style="height:5px;"></div>
    {bottom_html}
</div>
""", unsafe_allow_html=True)

st.caption("注：红色CH3代表甲基化修饰。启动子区域甲基化程度越高，基因表达越受抑制。")

# --- 6. 表型观察区 (重点修改部分) ---
st.markdown("---")
st.markdown('<div class="phenotype-section"><h3>🐭 表型观察</h3></div>', unsafe_allow_html=True)

# 根据滑块值决定显示哪只老鼠
if methylation_level < 30:
    # 黄色小鼠
    mouse_html = f'< img src="yellow.png" alt="黄色小鼠" style="width:200px; height:auto; border-radius:10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">'
    status = "黄色 (活跃)"
    conclusion_text = """
    - **状态：** 启动子低甲基化。
    - **机制：** 转录因子顺利结合，Agouti 基因持续高表达。
    - **结果：** 小鼠毛色呈现**黄色**，且易肥胖、易患糖尿病。
    """
elif methylation_level > 70:
    # 黑色小鼠
    mouse_html = f'< img src="black.png" alt="黑色小鼠" style="width:200px; height:auto; border-radius:10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">'
    status = "黑色 (沉默)"
    conclusion_text = """
    - **状态：** 启动子高甲基化。
    - **机制：** 甲基基团阻碍转录因子结合，Agouti 基因表达被抑制。
    - **结果：** 小鼠毛色呈现**黑色**，体型正常，健康状态良好。
    """
else:
    # 灰色小鼠 (中间状态)
    mouse_html = f'< img src="gray.png" alt="灰色小鼠" style="width:200px; height:auto; border-radius:10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">'
    status = "灰色 (中间态)"
    conclusion_text = """
    - **状态：** 启动子部分甲基化。
    - **机制：** 基因表达受到部分抑制，呈现杂色或中间色。
    - **结果：** 小鼠毛色呈现**灰色/杂色**，表型介于黄黑之间。
    """

# 使用 columns 布局让图片在中间，或者左右布局
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<div class="mouse-image-container">', unsafe_allow_html=True)
    # 关键点：必须加 unsafe_allow_html=True 才能显示图片
    st.markdown(mouse_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"**当前表型：{status}**")

# 实验结论
st.markdown('<div class="conclusion-box">', unsafe_allow_html=True)
st.markdown("#### 📝 实验结论")
st.markdown(conclusion_text)
st.markdown('</div>', unsafe_allow_html=True)
