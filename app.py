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
    promoter_length = 7
    total_rungs = len(DNA_TOP_SEQUENCE)

    methylated_count = int((level / 100) * promoter_length)
    methylated_indices = list(range(min(methylated_count, promoter_length)))

    svg = f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="background:#fff; border-radius:12px; border:1px solid #eee;">'

    # 背景区域
    svg += f'<rect x="50" y="40" width="380" height="180" fill="#E8F8F5" rx="10" opacity="0.8"/>'
    svg += f'<text x="240" y="70" text-anchor="middle" font-size="14" fill="#27AE60" font-weight="bold">启动子区域 (Promoter)</text>'
    svg += f'<rect x="440" y="40" width="310" height="180" fill="#EBF5FB" rx="10" opacity="0.8"/>'
    svg += f'<text x="590" y="70" text-anchor="middle" font-size="14" fill="#2980B9" font-weight="bold">编码区域 (Coding)</text>'

    # DNA绘制
    start_x = 80
    end_x = 720
    step = (end_x - start_x) / (total_rungs - 1)
    y_top = 120
    y_bottom = 180

    svg += f'<path d="M {start_x-10} {y_top-10} Q 400 {y_top-30} 750 {y_top-10}" fill="none" stroke="#2ECC71" stroke-width="6" stroke-linecap="round"/>'
    svg += f'<path d="M {start_x-10} {y_bottom+10} Q 400 {y_bottom+30} 750 {y_bottom+10}" fill="none" stroke="#2ECC71" stroke-width="6" stroke-linecap="round"/>'

    for i in range(total_rungs):
        cx = start_x + i * step
        top_base = DNA_TOP_SEQUENCE[i]
        bottom_base = DNA_BOTTOM_SEQUENCE[i]

        svg += f'<line x1="{cx}" y1="{y_top+5}" x2="{cx}" y2="{y_bottom-5}" stroke="#BDC3C7" stroke-width="1" stroke-dasharray="4,2"/>'
        svg += f'<text x="{cx}" y="{y_top}" text-anchor="middle" font-size="20" font-weight="bold" fill="#2C3E50">{top_base}</text>'
        svg += f'<text x="{cx}" y="{y_bottom+30}" text-anchor="middle" font-size="20" font-weight="bold" fill="#2C3E50">{bottom_base}</text>'

        # 绘制 CH3 标记
        if i in methylated_indices:
            svg += f'<circle cx="{cx}" cy="{y_top-30}" r="14" fill="#E74C3C"/>'
            svg += f'<text x="{cx}" y="{y_top-24}" text-anchor="middle" font-size="10" font-weight="bold" fill="white">CH3</text>'
            svg += f'<line x1="{cx}" y1="{y_top-16}" x2="{cx}" y2="{y_top-5}" stroke="#E74C3C" stroke-width="2"/>'

    svg += '</svg>'
    return svg

# --- 6. 页面布局展示 ---

# 分子结构区
st.markdown("### 🔬 分子结构观察")
st.markdown(draw_dna_structure(methylation_level), unsafe_allow_html=True)
st.caption("注：红色 CH3 代表甲基化修饰。启动子区域甲基化程度越高，基因表达越受抑制。")

st.markdown("---")

# --- 7. 表型观察区 (修复版：使用您的图片文件) ---
st.markdown("### 🐭 表型观察")
col_left, col_right = st.columns([1, 1.5])

with col_left:
    st.markdown("#### 小鼠毛色")

    # 检查图片是否存在
    image_path = "yellow.png"
    
    if os.path.exists(image_path):
        # --- 核心变色逻辑 ---
        # 我们使用 CSS 滤镜来模拟变色
        # 1. 亮度(brightness)：从 100% 降到 40%（变暗）
        # 2. 褐色化(sepia)：从 0% 升到 80%（变褐）
        # 3. 灰度(grayscale)：从 0% 升到 100%（变黑）
        
        brightness = 1.0 - (methylation_level / 100) * 0.6
        sepia = (methylation_level / 100) * 0.8
        grayscale = methylation_level / 100

        filter_style = f"filter: brightness({brightness}) sepia({sepia}) grayscale({grayscale}); transition: filter 0.3s ease;"

        # 使用 HTML 标签直接显示图片，确保路径正确
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            < img src="{image_path}" style="width: 200px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); {filter_style}">
        </div>
        """, unsafe_allow_html=True)
    else:
        # 如果没有图片，显示一个临时的 SVG 占位符
        st.warning("未找到 'yellow.png'，正在显示临时示意图。请确保图片文件在同级目录下。")
        st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <div style="width: 150px; height: 150px; background: {'#2C3E50' if methylation_level > 70 else '#F1C40F'}; border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">
                小鼠示意图
            </div>
        </div>
        """, unsafe_allow_html=True)

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
