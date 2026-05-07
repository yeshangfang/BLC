import streamlit as st

# --- 1. 页面配置 ---
st.set_page_config(page_title="Agouti基因甲基化模拟", layout="centered")

# --- 2. 固定数据定义 ---
# 预设一段固定的 DNA 序列（上链）
# 前7个为启动子区域，后7个为编码区域
FIXED_TOPLIST = ['A', 'T', 'G', 'C', 'A', 'G', 'T', 'C', 'G', 'A', 'T', 'C', 'G', 'A']
# 根据碱基互补配对原则生成的下链 (A-T, C-G)
FIXED_BOTTOMLIST = ['T', 'A', 'C', 'G', 'T', 'C', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T']

# --- 3. 核心绘图函数 ---
def draw_dna_structure(methylation_level):
    """
    绘制 DNA 结构
    逻辑：序列永远不变，只改变甲基化标记的显示
    """
    # 计算启动子区域（前7个）应该有多少个甲基化标记
    promoter_length = 7
    # 只有启动子区域会被甲基化
    methylated_count = int((methylation_level / 100) * promoter_length)

    # 生成当前状态下的甲基化位置列表（仅在前7个位置中随机）
    # 为了演示效果稳定，这里我们简单处理：总是从左边开始填充，或者随机
    # 这里采用随机抽样，但基于固定的范围
    import random
    methylated_indices = []
    if methylation_level > 0:
        # 在 0 到 6 的索引中随机选择
        methylated_indices = random.sample(range(promoter_length), methylated_count)

    # --- 开始绘制 HTML ---
    st.markdown("### 🧬 分子结构观察 (Agouti 基因启动子区)")

    # 使用 Flex 布局让 DNA 居中且紧凑
    st.markdown("""
        <style>
        .dna-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-family: 'Courier New', Courier, monospace;
            font-weight: bold;
            font-size: 18px;
            margin-bottom: 20px;
        }
        .dna-row {
            display: flex;
        }
        .base-unit {
            display: flex;
            flex-direction: column;
            align-items: center;
            width: 40px;
            margin: 0 2px;
            position: relative;
        }
        .base-letter {
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            border-radius: 50%;
            background-color: #f0f4f8;
            color: #2c3e50;
            z-index: 2;
        }
        .methyl-mark {
            width: 12px;
            height: 12px;
            background-color: #e74c3c; /* 红色甲基基团 */
            border-radius: 50%;
            margin-bottom: 2px;
            box-shadow: 0 0 5px #e74c3c;
            z-index: 3;
        }
        .spacer {
            width: 20px; /* 中间空隙 */
        }
        .region-label {
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .backbone {
            height: 40px;
            width: 2px;
            background-color: #95a5a6;
            margin: 0 5px;
        }
        </style>
    """, unsafe_allow_html=True)

    # 构建 HTML 字符串
    html_str = '<div class="dna-container">'

    # --- 上链 ---
    html_str += '<div class="region-label" style="align-self: flex-start; margin-left: 20px; color: #27ae60;">启动子区域 (Promoter)</div>'
    html_str += '<div class="dna-row">'

    for i in range(14):
        # 判断是否显示甲基化标记 (仅在启动子区 i < 7)
        show_methyl = (i in methylated_indices)

        html_str += '<div class="base-unit">'

        # 甲基化标记
        if show_methyl:
            html_str += '<div class="methyl-mark"></div>'
        else:
            html_str += '<div style="height:12px;"></div>' # 占位，保持高度一致

        # 碱基圆圈
        html_str += f'<div class="base-letter">{FIXED_TOPLIST[i]}</div>'

        html_str += '</div>' # end base-unit

        # 在 7 和 8 之间插入空隙
        if i == 6:
            html_str += '<div class="spacer"></div>'

    html_str += '</div>' # end dna-row

    # --- 连接线和下链 ---
    html_str += '<div class="dna-row" style="height: 10px; align-items: center;">'
    for i in range(14):
        html_str += '<div style="width:30px; border-top: 2px dotted #bdc3c7; margin: 0 2px;"></div>'
        if i == 6:
            html_str += '<div class="spacer"></div>'
    html_str += '</div>'

    html_str += '<div class="dna-row">'
    for i in range(14):
        html_str += '<div class="base-unit">'
        html_str += '<div style="height:12px;"></div>' # 下链上方留空
        html_str += f'<div class="base-letter">{FIXED_BOTTOMLIST[i]}</div>'
        html_str += '</div>'
        if i == 6:
            html_str += '<div class="spacer"></div>'
    html_str += '</div>'

    # --- 区域标注 ---
    html_str += '<div class="region-label" style="margin-top:10px; color: #2980b9; border-top: 1px solid #ccc; padding-top:5px; width: 100%; text-align:center;">编码区域 (Coding Sequence)</div>'

    html_str += '</div>' # end container

    st.markdown(html_str, unsafe_allow_html=True)

# --- 4. 主程序布局 ---

# 使用容器控制高度
with st.container():
    # --- 第一部分：控制区 ---
    st.markdown("### ⚙️ 实验参数设置")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("甲基化程度")
    with col2:
        methylation_level = st.slider("调节启动子甲基化水平", 0, 100, 0, label_visibility="collapsed")

    st.markdown("---") # 分割线

    # --- 第二部分：DNA 观察区 ---
    # 调用绘图函数，传入滑块的值，但函数内部保证序列不变
    draw_dna_structure(methylation_level)

    # --- 第三部分：结果区 ---
    st.markdown("### 🔬 表型与结论")
    col_res1, col_res2 = st.columns([1, 1])

    with col_res1:
        st.subheader("宏观表型")
        mouse_emoji, mouse_text, mouse_color = get_mouse_info(methylation_level)
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background-color: #f9f9f9; border-radius: 10px; border: 1px solid #eee;">
            <div style="font-size: 80px;">{mouse_emoji}</div>
            <div style="font-size: 18px; font-weight: bold; color: {mouse_color};">毛色: {mouse_text}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_res2:
        st.subheader("分子机制解释")
        if methylation_level > 60:
            st.info("🔴 **高度甲基化**\n\n启动子区域被大量甲基基团占据，阻碍了转录因子的结合。Agouti 基因**无法表达**，小鼠呈现**棕黄色**。")
        elif methylation_level > 30:
            st.warning("🟠 **部分甲基化**\n\n启动子区域部分被修饰，基因表达受到部分抑制，小鼠呈现**斑驳色**。")
        else:
            st.success("🟢 **低甲基化**\n\n启动子区域开放，转录因子顺利结合。Agouti 基因**正常表达**，小鼠呈现**黑色/伪黑色**。")

# --- 辅助函数 ---
def get_mouse_info(level):
    if level > 60:
        return "🐁", "棕黄色 (Agouti)", "#D2B48C"
    elif level > 30:
        return "🐁", "斑驳色 (Mottled)", "#8B7355"
    else:
        return "🐭", "黑色 (Pseudo-agouti)", "#2F4F4F"
