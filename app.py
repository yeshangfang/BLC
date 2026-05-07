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
    .block-container {padding-top: 2rem;}
    </style>
""", unsafe_allow_html=True)

# --- 4. 侧边栏/顶部控制 ---
st.title("🧬 表观遗传学模拟：Agouti 基因")
st.markdown("---")

col_ctrl_1, col_ctrl_2 = st.columns([1, 4])
with col_ctrl_1:
    st.markdown("### 实验参数")
with col_ctrl_2:
    methylation_level = st.slider(
        "调节启动子甲基化水平",
        0, 100, 0,
        label_visibility="collapsed"
    )

# 状态判断逻辑
if methylation_level < 30:
    status_text = "低甲基化 (基因活跃)"
    status_color = "#F1C40F" # 黄色
elif methylation_level < 70:
    status_text = "中等甲基化 (过渡型)"
    status_color = "#D35400" # 褐色
else:
    status_text = "高甲基化 (基因沉默)"
    status_color = "#2C3E50" # 黑色

st.markdown(f"""
<div style="text-align: center; margin-bottom: 20px;">
    <span style="color: {status_color}; font-weight: bold; font-size: 1.1em;">● {status_text}</span>
</div>
""", unsafe_allow_html=True)

# --- 5. 核心功能：绘制DNA结构 ---
def draw_dna_structure(level):
    width = 800
    height = 260
    promoter_length = 7  # 前7个碱基为启动子
    total_rungs = len(DNA_TOP_SEQUENCE)

    # 计算甲基化数量 (简单的线性映射)
    methylated_count = int((level / 100) * promoter_length)

    # 随机选择甲基化的位置 (仅在启动子区域)
    methylated_indices = list(range(min(methylated_count, promoter_length)))

    # SVG 开始
    svg = f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#fff; border-radius:12px; border:1px solid #eee;">'

    # 1. 绘制背景区域
    # 启动子区 (淡绿)
    svg += f'<rect x="50" y="40" width="380" height="180" fill="#E8F8F5" rx="10" opacity="0.8"/>'
    svg += f'<text x="240" y="70" text-anchor="middle" font-size="14" fill="#27AE60" font-weight="bold">启动子区域 (Promoter)</text>'

    # 编码区 (淡蓝)
    svg += f'<rect x="440" y="40" width="310" height="180" fill="#EBF5FB" rx="10" opacity="0.8"/>'
    svg += f'<text x="590" y="70" text-anchor="middle" font-size="14" fill="#2980B9" font-weight="bold">编码区域 (Coding)</text>'

    # 2. 绘制DNA骨架和碱基
    start_x = 80
    end_x = 720
    step = (end_x - start_x) / (total_rungs - 1)
    y_top = 120
    y_bottom = 180

    # 骨架线条 (柔和绿)
    svg += f'<path d="M {start_x-10} {y_top-10} Q 400 {y_top-30} 750 {y_top-10}" fill="none" stroke="#2ECC71" stroke-width="6" stroke-linecap="round"/>'
    svg += f'<path d="M {start_x-10} {y_bottom+10} Q 400 {y_bottom+30} 750 {y_bottom+10}" fill="none" stroke="#2ECC71" stroke-width="6" stroke-linecap="round"/>'

    for i in range(total_rungs):
        cx = start_x + i * step
        top_base = DNA_TOP_SEQUENCE[i]
        bottom_base = DNA_BOTTOM_SEQUENCE[i]

        # 绘制氢键 (虚线)
        svg += f'<line x1="{cx}" y1="{y_top+5}" x2="{cx}" y2="{y_bottom-5}" stroke="#BDC3C7" stroke-width="1" stroke-dasharray="4,2"/>'

        # 绘制上链碱基
        svg += f'<text x="{cx}" y="{y_top}" text-anchor="middle" font-size="20" font-weight="bold" fill="#2C3E50">{top_base}</text>'
        # 绘制下链碱基
        svg += f'<text x="{cx}" y="{y_bottom+30}" text-anchor="middle" font-size="20" font-weight="bold" fill="#2C3E50">{bottom_base}</text>'

        # 绘制甲基化标记 (CH3) - 仅在启动子区域
        if i in methylated_indices:
            # CH3 红色圆底
            svg += f'<circle cx="{cx}" cy="{y_top-30}" r="14" fill="#E74C3C"/>'
            # CH3 文字 (白色)
            svg += f'<text x="{cx}" y="{y_top-24}" text-anchor="middle" font-size="10" font-weight="bold" fill="white">CH3</text>'
            # 连接线
            svg += f'<line x1="{cx}" y1="{y_top-16}" x2="{cx}" y2="{y_top-5}" stroke="#E74C3C" stroke-width="2"/>'

    svg += '</svg>'
    return svg

# --- 6. 页面布局展示 ---

# 分子结构区
st.markdown("### 🔬 分子结构观察")
st.markdown(draw_dna_structure(methylation_level), unsafe_allow_html=True)
st.caption("注：红色圆底上的 **CH3** 代表甲基化修饰。启动子区域甲基化程度越高，基因表达越受抑制。")

st.markdown("---")

# 表型观察区
st.markdown("### 🐭 表型观察")
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown("#### 小鼠毛色")

    # 核心逻辑：利用 CSS 滤镜实现从黄色图片到黑色的平滑过渡
    # 当 level=0 (全黄) -> brightness(1) grayscale(0)
    # 当 level=100 (全黑) -> brightness(0.3) grayscale(1)

    # 计算滤镜参数
    # 亮度：1.0 (正常) -> 0.2 (暗)
    brightness = 1.0 - (methylation_level / 100) * 0.8
    # 灰度：0 (彩色) -> 1 (黑白/深色)
    grayscale = methylation_level / 100

    filter_style = f"filter: brightness({brightness}) grayscale({grayscale}); border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: filter 0.3s ease;"

    try:
        # 使用 HTML 包裹图片以应用动态样式
        st.markdown(f"""
        <div style="text-align: center; margin-top: 20px;">
            < img src="yellow.png" style="width: 70%; {filter_style}">
            <p style="font-size: 0.9em; color: #666; margin-top: 10px;">基于黄色小鼠原图的动态着色</p >
        </div>
        """, unsafe_allow_html=True)

    except Exception:
        st.warning("未找到 'yellow.png'，请确保图片在同一目录下。")

with col_right:
    st.markdown("#### 实验结论")
    if methylation_level > 70:
        st.success(f"""
        **✅ 基因沉默 (黑色)**
        - **状态**：启动子高度甲基化。
        - **机制**：甲基基团阻碍了转录因子结合，Agouti 基因无法表达。
        - **结果**：小鼠毛色呈现**黑色**，体型健康。
        """)
    elif methylation_level < 30:
        st.error(f"""
        **⚠️ 基因活跃 (黄色)**
        - **状态**：启动子低甲基化。
        - **机制**：转录因子顺利结合，Agouti 基因持续高表达。
        - **结果**：小鼠毛色呈现**黄色**，且易肥胖、易患糖尿病。
        """)
    else:
        st.info(f"""
        **⚖️ 过渡状态 (褐色)**
        - **状态**：部分甲基化。
        - **结果**：基因表达受到部分抑制，毛色介于黄黑之间。
        """)
