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
# 使用 f-string 将 python 变量 methylation_level 注入到 CSS 中
st.markdown(f"""
    <style>
    /* 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    body {{
        background-color: #F7F9FA;
        font-family: 'Inter', sans-serif;
        color: #333;
    }}
    /* 卡片容器 */
    .card {{
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        padding: 24px;
        margin-bottom: 20px;
        border: 1px solid #E0E0E0;
    }}
    /* DNA 碱基样式 */
    .base {{
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        font-weight: 600;
        font-size: 14px;
        z-index: 2;
    }}
    .base-A {{ background-color: #FF6B6B; color: white; }} /* 红 */
    .base-T {{ background-color: #4ECDC4; color: white; }} /* 青 */
    .base-C {{ background-color: #FFD93D; color: #333; }} /* 黄 */
    .base-G {{ background-color: #1A535C; color: white; }} /* 深青 */

    /* DNA 骨架线 */
    .backbone {{
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        background-color: #333;
        z-index: 0;
    }}
    .top-backbone {{ top: 10px; height: 12px; }}
    .bottom-backbone {{ bottom: 10px; height: 12px; }}

    /* 碱基对连接线 */
    .connector {{
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 24px;
        background-color: #A0A0A0;
        z-index: 1;
    }}
    /* 氢键虚线模拟 (仅视觉示意) */
    .h-bond {{
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 24px;
        background: repeating-linear-gradient(
            to bottom,
            #A0A0A0,
            #A0A0A0 2px,
            transparent 2px,
            transparent 4px
        );
        z-index: 1;
    }}

    /* 甲基化标记 CH3 */
    .methyl-group {{
        position: absolute;
        top: -28px; /* 调整位置使其在碱基上方 */
        left: 50%;
        transform: translateX(-50%);
        font-size: 12px;
        font-weight: bold;
        color: #D62828; /* 深红色文字 */
        font-family: monospace;
        background: rgba(255, 255, 255, 0.8);
        padding: 2px 4px;
        border-radius: 4px;
        border: 1px solid #D62828;
        z-index: 3;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 24px;
    }}
    /* CH3 连接线 */
    .methyl-line {{
        position: absolute;
        top: -4px;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 8px;
        background-color: #D62828;
        z-index: 2;
    }}

    /* 小鼠容器 */
    .mouse-container {{
        position: relative;
        width: 200px;
        height: 200px;
        margin: 0 auto;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid #ddd;
        background-color: #fff;
    }}
    /* 小鼠图片 */
    .mouse-img {{
        width: 100%;
        height: 100%;
        object-fit: contain;
        /* 关键：使用亮度滤镜模拟变色。
           0% = 原图(黄), 100% = 黑。
           我们将滑块值(0-100)直接映射给滤镜 */
        filter: brightness(calc(1 - {methylation_level} / 100 * 0.85));
        transition: filter 0.3s ease;
    }}

    /* 实验结论高亮 */
    .conclusion-box {{
        background-color: #E3F2FD;
        border-left: 5px solid #2196F3;
        padding: 15px;
        border-radius: 4px;
        font-size: 14px;
        line-height: 1.6;
    }}
    .tag {{
        display: inline-block;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 12px;
        color: white;
        margin-right: 5px;
    }}
    .tag-yellow {{ background-color: #FFC107; }}
    .tag-brown {{ background-color: #795548; }}
    .tag-black {{ background-color: #424242; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. 页面布局 ---

# 标题
st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🐭 Agouti 基因甲基化模拟</h2>", unsafe_allow_html=True)

# A. DNA 结构可视化 (HTML)
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; font-weight: 600; margin-bottom: 20px; color: #555;'>DNA 序列结构 (Agouti 基因启动子区)</div>", unsafe_allow_html=True)

# 构建 DNA 的 HTML
dna_html = "<div style='position: relative; height: 80px; width: 500px; margin: 0 auto; display: flex; justify-content: space-around; align-items: center;'>"

# 左侧骨架线
dna_html += "<div class='backbone top-backbone' style='height: 60px; left: 0; transform: none;'></div>"
dna_html += "<div class='backbone bottom-backbone' style='height: 60px; left: 0; transform: none;'></div>"
# 右侧骨架线
dna_html += "<div class='backbone top-backbone' style='height: 60px; right: 0; left: auto; transform: none;'></div>"
dna_html += "<div class='backbone bottom-backbone' style='height: 60px; right: 0; left: auto; transform: none;'></div>"

for i, base_top in enumerate(DNA_TOP_SEQUENCE):
    base_bottom = DNA_BOTTOM_SEQUENCE[i]

    # 计算位置百分比
    pos = (i / (len(DNA_TOP_SEQUENCE) - 1)) * 100

    # 随机决定此位点是否甲基化 (基于滑块概率)
    # 如果滑块是 80%，则每个位点有 80% 概率显示 CH3
    is_methylated = random.randint(0, 99) < methylation_level

    # --- 上链 ---
    dna_html += f"""
    <div style="position: absolute; left: {pos}%; transform: translateX(-50%); display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: space-between;">
        <!-- 甲基化标记 CH3 -->
        {'<div class="methyl-group">CH3</div><div class="methyl-line"></div>' if is_methylated else '<div style="height: 28px;"></div>'}

        <div class="base base-{base_top}">{base_top}</div>
        <div class="{'h-bond' if base_top in ['A', 'T'] else 'connector'}"></div>
        <div class="base base-{base_bottom}">{base_bottom}</div>
    </div>
    """

dna_html += "</div>"
st.markdown(dna_html, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; font-size: 12px; color: #888; margin-top: 15px;'>注：红色 CH3 代表甲基化修饰。滑块数值越高，出现 CH3 的概率越大。</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True) # Close Card

# B. 表型与结论区域
col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='card' style='text-align: center;'>", unsafe_allow_html=True)
    st.markdown("### 🖼️ 表型观察")
    st.markdown("<div class='mouse-container'>", unsafe_allow_html=True)
    # 使用 HTML img 标签确保图片加载，利用 CSS 滤镜变色
    st.markdown(f'< img src="yellow.png" class="mouse-img" alt="Mouse">', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 根据数值显示不同状态
    status = ""
    if methylation_level < 30:
        status = "黄色 (未甲基化)"
    elif methylation_level < 70:
        status = "杂色/褐色 (部分甲基化)"
    else:
        status = "黑色 (高度甲基化)"

    st.markdown(f"<p style='margin-top:15px; font-weight:bold;'>当前表型：**{status}**</p >", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📝 实验结论")

    conclusion_text = ""
    if methylation_level < 30:
        conclusion_text = """
        <div class='conclusion-box'>
            <p><strong>当前状态：</strong> <span class='tag tag-yellow'>低甲基化</span></p >
            <p><strong>机制分析：</strong> Agouti 基因启动子区域<strong>未甲基化</strong>，RNA聚合酶可以顺利结合。</p >
            <p><strong>结果：</strong> Agouti 基因<strong>持续高表达</strong>，抑制了黑色素的合成，小鼠毛色呈现<strong>黄色</strong>，且容易肥胖。</p >
        </div>
        """
    elif methylation_level < 70:
        conclusion_text = """
        <div class='conclusion-box'>
            <p><strong>当前状态：</strong> <span class='tag tag-brown'>中等甲基化</span></p >
            <p><strong>机制分析：</strong> Agouti 基因启动子区域发生<strong>部分甲基化</strong>。</p >
            <p><strong>结果：</strong> 基因表达受到部分抑制，毛色在黄色和黑色之间波动，呈现<strong>杂色/褐色</strong>。</p >
        </div>
        """
    else:
        conclusion_text = """
        <div class='conclusion-box'>
            <p><strong>当前状态：</strong> <span class='tag tag-black'>高甲基化</span></p >
            <p><strong>机制分析：</strong> Agouti 基因启动子区域<strong>高度甲基化</strong>，阻碍了转录因子的结合。</p >
            <p><strong>结果：</strong> Agouti 基因表达被<strong>沉默 (Silenced)</strong>，无法抑制黑色素合成，小鼠毛色呈现<strong>黑色/伪黑色</strong>，且体型健康。</p >
        </div>
        """

    st.markdown(conclusion_text, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 底部说明
st.markdown("<div style='text-align: center; margin-top: 30px; color: #999; font-size: 12px;'>模拟演示：表观遗传学对基因表达的调控</div>", unsafe_allow_html=True)
