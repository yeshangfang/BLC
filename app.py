import streamlit as st
import random

# --- 1. 页面设置与全局样式 ---
st.set_page_config(page_title="Agouti基因甲基化模拟", layout="centered")

# 注入自定义CSS以控制高度和字体
st.markdown("""
    <style>
    /* 全局字体设置 */
    html, body, [class*="css"] {
        font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
    }

    /* 减少顶部默认填充，确保内容能塞进屏幕 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 800px; /* 限制最大宽度，防止在大屏上太散 */
    }

    /* 标题样式 */
    h1 {
        font-size: 28px;
        font-weight: 700;
        color: #2C3E50;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    /* 小标题样式 */
    h3 {
        font-size: 18px;
        color: #34495E;
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 5px;
        margin-top: 10px;
    }

    /* 调节滑块文字 */
    .stSlider label {
        font-size: 18px;
        font-weight: 600;
        color: #2C3E50;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. 核心数据：DNA序列 ---
# 预设一段真实的序列，确保碱基互补配对 (A-T, C-G)
# 左侧7个碱基为启动子区域，右侧为编码区
DNA_SEQUENCE_TOP = "T A C G G T A C G T A C G G"
DNA_SEQUENCE_BOT = "A T G C C A T G C A T G C C" # 严格互补
TOTAL_LEN = len(DNA_SEQUENCE_TOP.split())
PROMOTER_LEN = 7 # 启动子长度

# --- 3. 侧边栏或顶部：调节模块 (占 1/4 视觉重心) ---
st.title("🧬 表观遗传学：Agouti 基因模拟")

# 使用容器控制布局
with st.container():
    # 居中显示调节器
    col_c1, col_c2, col_c3 = st.columns([1, 6, 1])
    with col_c2:
        st.markdown("### ⚙️ 实验参数设置")
        methylation_level = st.slider(
            "调节启动子甲基化程度",
            min_value=0,
            max_value=100,
            value=0,
            help="拖动滑块模拟不同环境下的甲基化水平"
        )

        # 根据数值显示状态
        if methylation_level == 0:
            status = "🟢 无甲基化 (基因活跃)"
            status_color = "#27AE60"
        elif methylation_level < 40:
            status = "🟡 低甲基化 (基因较活跃)"
            status_color = "#F1C40F"
        elif methylation_level < 70:
            status = "🟠 中等甲基化 (基因受抑)"
            status_color = "#E67E22"
        else:
            status = "🔴 高甲基化 (基因沉默)"
            status_color = "#C0392B"

        st.markdown(f"<p style='text-align: center; color: {status_color}; font-weight: bold; font-size: 16px;'>当前状态：{status}</p >", unsafe_allow_html=True)

st.markdown("---") # 分割线

# --- 4. 底部：展示模块 (占 3/4 视觉重心) ---
# 这里我们将 DNA 图和 结果图 并列或上下紧凑排列

# 第一行：DNA 分子结构可视化
st.markdown("### 🔬 分子结构观察")

# 计算甲基化位点 (仅在启动子区域随机分布)
methylated_indices = []
if methylation_level > 0:
    # 计算需要点亮的红点数量
    num_dots = max(1, int((methylation_level / 100) * PROMOTER_LEN))
    # 在前7个位置(启动子)中随机选择
    methylated_indices = random.sample(range(PROMOTER_LEN), num_dots)

# 绘制 DNA (使用 HTML/CSS 表格布局确保对齐)
dna_html = """
<div style="display: flex; justify-content: center; margin-top: 20px;">
    <div style="background-color: #fff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); font-family: monospace;">
        <div style="display: flex; flex-direction: column; align-items: center;">
            <!-- 区域标签 -->
            <div style="width: 100%; display: flex; justify-content: center; margin-bottom: 5px; font-size: 12px; font-weight: bold; color: #7f8c8d;">
                <div style="width: 50%; text-align: center; color: #2980b9;">启动子区域 (Promoter)</div>
                <div style="width: 50%; text-align: center; color: #8e44ad;">编码区域 (Coding)</div>
            </div>

            <!-- DNA 结构主体 -->
            <div style="display: flex; align-items: center; font-size: 20px; font-weight: bold;">
"""

# 生成碱基对循环
top_bases = DNA_SEQUENCE_TOP.split()
bot_bases = DNA_SEQUENCE_BOT.split()

for i in range(TOTAL_LEN):
    # 判断背景色区域
    if i < PROMOTER_LEN:
        bg_color = "#EBF5FB" # 浅蓝 (启动子)
        border_side = "border-right: 2px solid #fff;"
    else:
        bg_color = "#F4ECF7" # 浅紫 (编码区)
        border_side = ""

    # 判断是否有甲基化标记
    dot_html = ""
    if i in methylated_indices:
        dot_html = '<div style="color: #E74C3C; font-size: 24px; line-height: 10px;">•</div>'
    else:
        dot_html = '<div style="height: 24px;"></div>' # 占位符保持对齐

    # 单个碱基对单元
    dna_html += f"""
        <div style="display: flex; flex-direction: column; align-items: center; margin: 0 4px; background-color: {bg_color}; padding: 5px 8px; border-radius: 8px; {border_side}">
            {dot_html} <!-- 甲基化红点 -->
            <div style="color: #2C3E50;">{top_bases[i]}</div> <!-- 上链 -->
            <div style="height: 4px; border-bottom: 2px solid #BDC3C7; width: 80%; margin: 2px 0;"></div> <!-- 氢键 -->
            <div style="color: #2C3E50;">{bot_bases[i]}</div> <!-- 下链 -->
        </div>
    """

# 闭合 HTML
dna_html += """
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #95A5A6; text-align: center;">
                注：红色圆点代表甲基基团(-CH3)，仅出现在启动子区域
            </div>
        </div>
    </div>
</div>
"""
st.markdown(dna_html, unsafe_allow_html=True)

st.markdown("---")

# 第二行：表型与结论
col_res1, col_res2 = st.columns([1, 1])

with col_res1:
    st.markdown("### 🐭 宏观表型")
    # 根据甲基化程度决定小鼠颜色
    # 甲基化高 -> 基因沉默 -> 无法合成黄色素 -> 黑色/灰色
    # 甲基化低 -> 基因表达 -> 合成黄色素 -> 黄色/肥胖
    if methylation_level > 70:
        st.image(IMG_BLACK, width=150) # 假设你有黑色小鼠图，或者用灰色代替
        st.caption("毛色：黑色/灰色 (健康)")
    elif methylation_level > 30:
        st.image(IMG_GRAY, width=150) # 杂色
        st.caption("毛色：斑驳色 (中等)")
    else:
        st.image(IMG_WHITE, width=150) # 假设白色代表黄色(因为我没有黄色图，用白色代替示意)
        st.caption("毛色：黄色 (肥胖/易患病)")

with col_res2:
    st.markdown("### 📝 实验结论")
    with st.container(border=True):
        if methylation_level > 70:
            st.success("**基因表达被抑制**")
            st.markdown("""
            - **机制**：启动子区域被大量甲基基团占据。
            - **结果**：RNA聚合酶无法结合，Agouti 基因**沉默**。
            - **现象**：小鼠无法合成黄色素，表现为**黑色/灰色**，体型正常。
            """)
        else:
            st.warning("**基因表达活跃**")
            st.markdown("""
            - **机制**：启动子区域甲基化程度低，无阻碍。
            - **结果**：RNA聚合酶顺利结合，Agouti 基因**持续转录**。
            - **现象**：小鼠持续合成黄色素，表现为**黄色**，且易肥胖。
            """)
