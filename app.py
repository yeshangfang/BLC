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
    </style>
""", unsafe_allow_html=True)

# --- 4. 核心功能：绘制DNA结构 ---
def draw_dna_structure(level):
    # 莫兰迪配色
    PROMOTER_BG = "#E8F1F2" # 启动子背景 (淡蓝绿)
    CODING_BG = "#D5E1DF"   # 编码区背景 (灰绿)
    STRAND_COLOR = "#2C3E50" # 骨架颜色
    BASE_COLOR = "#2C3E50"
    METHYL_COLOR = "#E74C3C" # 甲基化红色

    total_rungs = 14
    promoter_length = 7

    # 计算当前甲基化数量 (0-100% 映射到 0-7个位点)
    # 这里为了演示效果，我们让甲基化点随机分布，但总数随level增加
    import random
    methylated_count = int((level / 100) * promoter_length)

    # 随机选取哪些位点被甲基化
    methylated_positions = random.sample(range(promoter_length), methylated_count) if level > 0 else []

    width = 800
    height = 220
    # 使用SVG绘制DNA
    svg = f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="border-radius: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); background: white;">'

    # 1. 绘制背景区域
    svg += f'<rect x="50" y="40" width="370" height="140" fill="{PROMOTER_BG}" rx="10" />'
    svg += f'<text x="235" y="70" text-anchor="middle" fill="#7F8C8D" font-size="12" font-family="sans-serif">启动子区域 (Promoter)</text>'

    svg += f'<rect x="430" y="40" width="320" height="140" fill="{CODING_BG}" rx="10" />'
    svg += f'<text x="590" y="70" text-anchor="middle" fill="#7F8C8D" font-size="12" font-family="sans-serif">编码区域 (Coding)</text>'

    # 2. 绘制骨架
    svg += f'<path d="M 60 80 Q 400 40 740 80" fill="none" stroke="{STRAND_COLOR}" stroke-width="4" />'
    svg += f'<path d="M 60 140 Q 400 180 740 140" fill="none" stroke="{STRAND_COLOR}" stroke-width="4" />'

    # 3. 绘制碱基和氢键
    step = (740 - 60) / (total_rungs + 1)

    for i in range(total_rungs):
        cx = 60 + (i + 1) * step
        top_base = DNA_TOP_SEQUENCE[i]
        bottom_base = DNA_BOTTOM_SEQUENCE[i]

        # 氢键
        svg += f'<line x1="{cx}" y1="90" x2="{cx}" y2="130" stroke="#BDC3C7" stroke-width="1" stroke-dasharray="2,2"/>'

        # 上链碱基
        svg += f'<text x="{cx}" y="85" text-anchor="middle" fill="{BASE_COLOR}" font-size="16" font-weight="bold" font-family="Arial">{top_base}</text>'
        # 下链碱基
        svg += f'<text x="{cx}" y="155" text-anchor="middle" fill="{BASE_COLOR}" font-size="16" font-weight="bold" font-family="Arial">{bottom_base}</text>'

        # 4. 绘制甲基化标记 (CH3) - 仅在启动子区域
        if i in methylated_positions:
            # 连接线
            svg += f'<line x1="{cx}" y1="60" x2="{cx}" y2="78" stroke="{METHYL_COLOR}" stroke-width="2" />'
            # CH3 文字
            svg += f'<text x="{cx}" y="55" text-anchor="middle" fill="{METHYL_COLOR}" font-size="14" font-weight="bold" font-family="sans-serif">CH3</text>'
            # 红色小圆点装饰
            svg += f'<circle cx="{cx}" cy="55" r="3" fill="{METHYL_COLOR}" />'

    svg += '</svg>'
    return svg

# --- 5. 主程序布局 ---

st.markdown("<h2 style='text-align: center; margin-bottom: 1rem;'>🧬 Agouti 基因甲基化模拟</h2>", unsafe_allow_html=True)

# 滑块控制
methylation_level = st.slider("调节启动子甲基化水平", 0, 100, 0, label_visibility="collapsed")

# 显示DNA
st.markdown(draw_dna_structure(methylation_level), unsafe_allow_html=True)
st.caption("注：红色 CH3 代表甲基化修饰。启动子区域甲基化程度越高，基因表达越受抑制。")

st.markdown("---")

# --- 6. 表型观察区域 ---
col1, col2 = st.columns([1, 1])

# 计算颜色深浅 (0% 到 80% 的黑色遮罩)
# 使用线性插值：level=0 -> opacity=0 (全黄), level=100 -> opacity=0.8 (全黑)
overlay_opacity = methylation_level * 0.008

# 判断表型文字
if methylation_level < 30:
    phenotype = "黄色 (肥胖)"
    status = "基因活跃表达"
    color_desc = "启动子未甲基化，Agouti基因持续表达。"
elif methylation_level < 70:
    phenotype = "褐色/杂色 (中等)"
    status = "基因部分抑制"
    color_desc = "启动子部分甲基化，Agouti基因表达受部分抑制。"
else:
    phenotype = "黑色 (健康)"
    status = "基因完全沉默"
    color_desc = "启动子高度甲基化，Agouti基因无法表达。"

with col1:
    st.subheader("🐭 表型观察")
    st.markdown("**小鼠毛色**")

    # 核心修复：使用 HTML 直接控制图片叠加和滤镜
    # 我们使用 yellow.png 作为底图，上面覆盖一个透明度可控的黑色层
    mouse_html = f"""
    <div style="position: relative; width: 250px; height: 250px; margin: 0 auto; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
        <!-- 底层：黄色小鼠图片 -->
        < img src="yellow.png" style="width: 100%; height: 100%; object-fit: cover; display: block;">
        <!-- 顶层：黑色遮罩，透明度随滑块变化 -->
        <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-color: black; opacity: {overlay_opacity}; pointer-events: none;"></div>
    </div>
    <p style="text-align: center; font-weight: bold; margin-top: 10px;">当前表型：{phenotype}</p >
    """
    st.markdown(mouse_html, unsafe_allow_html=True)

with col2:
    st.subheader("📝 实验结论")
    st.info(f"""
    **当前状态：{status}**
    - **甲基化水平**：{methylation_level}%
    - **解释**：{color_desc}
    """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #95A5A6; font-size: 0.8em;'>DNA Methylation Simulator v3.0 (Fixed)</div>", unsafe_allow_html=True)
