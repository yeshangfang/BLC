import streamlit as st
import random

# --- 1. 页面设置与自定义CSS ---
st.set_page_config(page_title="DNA启动子甲基化模拟", layout="centered", initial_sidebar_state="collapsed")

# 高级感配色与布局CSS
st.markdown("""
    <style>
    /* 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    body {
        background-color: #F7F9FA; /* 柔和的米灰背景 */
        font-family: 'Inter', sans-serif;
        color: #2C3E50;
    }
    
    /* 隐藏顶部默认的Streamlit菜单，让页面更整洁 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 卡片式容器 */
    .css-1r6slb0 {
        background: transparent;
    }
    
    /* 滑块样式优化 */
    .stSlider > div > div > div > div {
        background-color: #5D6D7E !important; /* 深色滑块轨道 */
    }
    
    /* 标题样式 */
    h1, h2, h3, h4 {
        font-weight: 600;
        color: #2C3E50;
        letter-spacing: -0.5px;
    }
    
    /* 紧凑布局调整 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 图片文件名设置 ---
# 请确保同级目录下有这三张图片，如果没有代码会自动显示占位符
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 核心功能：绘制高级感 DNA 结构 ---
def draw_dna_structure(level):
    """
    绘制横向 DNA 结构，采用莫兰迪配色
    """
    # 莫兰迪配色方案
    PROMOTER_BG = "#D5E1DF"  # 鼠尾草绿 (启动子)
    CODING_BG = "#D6E2E9"    # 雾霾蓝 (编码区)
    METHYL_COLOR = "#E07A5F" # 珊瑚红 (甲基化)
    TEXT_COLOR = "#3D405B"   # 深蓝灰 (文字)
    STRAND_COLOR = "#81B29A" # 柔和绿 (骨架)

    total_rungs = 14
    promoter_length = 7
    methylated_count = int((level / 100) * promoter_length)

    # 随机生成甲基化位置
    methylated_positions = []
    if level > 0:
        possible_indices = list(range(promoter_length))
        count = max(1, methylated_count) if level <= 60 else promoter_length
        methylated_positions = random.sample(possible_indices, min(count, len(possible_indices)))

    # 开始构建 SVG
    width = 850
    height = 240
    svg = f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1)); border-radius: 12px;">'
    
    # 背景区域划分
    # 启动子背景
    svg += f'<rect x="20" y="20" width="400" height="200" fill="{PROMOTER_BG}" rx="10" ry="10" opacity="0.6"/>'
    # 编码区背景
    svg += f'<rect x="430" y="20" width="400" height="200" fill="{CODING_BG}" rx="10" ry="10" opacity="0.6"/>'
    
    # 区域标签
    svg += f'<text x="220" y="50" text-anchor="middle" fill="{TEXT_COLOR}" font-size="14" font-weight="bold" letter-spacing="1">启动子区域 (Promoter)</text>'
    svg += f'<text x="630" y="50" text-anchor="middle" fill="{TEXT_COLOR}" font-size="14" font-weight="bold" letter-spacing="1">编码区域 (Coding)</text>'

    # 绘制 DNA 骨架
    y_top = 100
    y_bottom = 160
    start_x = 50
    end_x = 800
    
    svg += f'<path d="M {start_x} {y_top} Q 425 {y_top-10} 800 {y_top}" fill="none" stroke="{STRAND_COLOR}" stroke-width="6" stroke-linecap="round"/>'
    svg += f'<path d="M {start_x} {y_bottom} Q 425 {y_bottom+10} 800 {y_bottom}" fill="none" stroke="{STRAND_COLOR}" stroke-width="6" stroke-linecap="round"/>'

    # 绘制碱基对
    bases = ["A", "T", "C", "G"]
    step = (end_x - start_x) / (total_rungs + 1)

    for i in range(total_rungs):
        cx = start_x + (i + 1) * step
        
        # 随机碱基
        base = random.choice(bases)
        
        # 绘制氢键
        svg += f'<line x1="{cx}" y1="{y_top+15}" x2="{cx}" y2="{y_bottom-15}" stroke="#F2F2F2" stroke-width="2" stroke-dasharray="4,4"/>'
        
        # 绘制碱基文字
        svg += f'<text x="{cx}" y="{y_top}" text-anchor="middle" fill="{TEXT_COLOR}" font-size="18" font-weight="bold" font-family="Arial">{base}</text>'
        svg += f'<text x="{cx}" y="{y_bottom+25}" text-anchor="middle" fill="{TEXT_COLOR}" font-size="18" font-weight="bold" font-family="Arial">{base}</text>'

        # 绘制甲基化标记 (红色圆点)
        if i in methylated_positions:
            # 圆点
            svg += f'<circle cx="{cx}" cy="{y_top-25}" r="10" fill="{METHYL_COLOR}" />'
            # 化学键连接线
            svg += f'<line x1="{cx}" y1="{y_top-15}" x2="{cx}" y2="{y_top-5}" stroke="{METHYL_COLOR}" stroke-width="2"/>'
            # 文字
            svg += f'<text x="{cx}" y="{y_top-20}" text-anchor="middle" fill="white" font-size="10" font-weight="bold">CH3</text>'

    svg += '</svg>'
    return svg

# --- 4. 主程序布局 ---

# 顶部标题
st.title("🧬 表观遗传学模拟：Agouti 基因")

# --- 第一部分：调节模块 (顶部 1/4) ---
# 使用 columns 控制宽度，使其看起来更精致
col_ctrl_1, col_ctrl_2 = st.columns([1, 4])
with col_ctrl_1:
    st.markdown("### 实验参数")
with col_ctrl_2:
    methylation_level = st.slider(
        "调节启动子甲基化水平", 
        0, 100, 0, 
        label_visibility="collapsed"
    )

# 状态指示条
status_text = ""
status_color = ""
if methylation_level < 30:
    status_text = "低甲基化状态 (基因活跃)"
    status_color = "#81B29A" # 绿色
elif methylation_level < 70:
    status_text = "中等甲基化状态"
    status_color = "#F2CC8F" # 黄色
else:
    status_text = "高甲基化状态 (基因沉默)"
    status_color = "#E07A5F" # 红色

st.markdown(f"""
<div style="text-align: center; margin-top: -20px; margin-bottom: 10px;">
    <span style="color: {status_color}; font-weight: bold; font-size: 1.1em;">● {status_text}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 第二部分：DNA 结构 (中间核心) ---
st.markdown("### 分子结构观察")
# 使用容器包裹，增加内边距
with st.container():
    st.markdown(draw_dna_structure(methylation_level), unsafe_allow_html=True)
    st.caption("图注：绿色背景区域为启动子，蓝色背景区域为编码区。红色圆点代表抑制基因表达的甲基化修饰。")

# --- 第三部分：结果与结论 (底部 1/2) ---
st.markdown("### 表型与结论")
col_result_left, col_result_right = st.columns(2)

# 逻辑判断
is_silenced = methylation_level > 60

with col_result_left:
    st.markdown("#### 宏观表型")
    # 尝试显示图片，如果文件不存在则显示文字
    try:
        if is_silenced:
            st.image(IMG_BLACK, caption="黑色/褐色 (健康)", width=250)
        else:
            st.image(IMG_YELLOW if 'IMG_YELLOW' in locals() else IMG_GRAY, caption="黄色 (肥胖)", width=250)
    except:
        st.write(f"**{'黑色' if is_silenced else '黄色'}**")

with col_result_right:
    st.markdown("#### 实验结论")
    if is_silenced:
        st.success("""
        **✅ 基因表达被抑制**
        - **机制**：启动子区域被大量甲基基团（-CH3）占据。
        - **结果**：RNA聚合酶无法结合，Agouti 基因无法转录。
        - **现象**：小鼠无法合成黄色素，毛色呈现正常的黑色。
        """)
    else:
        st.error("""
        **⚠️ 基因持续表达**
        - **机制**：启动子区域干净，无甲基化修饰。
        - **结果**：转录因子顺利结合，Agouti 基因持续活跃转录。
        - **现象**：小鼠合成大量黄色素，毛色呈现黄色且易肥胖。
        """)

# 底部极简页脚
st.markdown("---")
st.markdown("<div style='text-align: center; color: #95A5A6; font-size: 0.8em;'>DNA Methylation Simulator v2.0</div>", unsafe_allow_html=True)
