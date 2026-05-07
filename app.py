import streamlit as st
import time

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA甲基化模拟器", layout="centered")

# --- 2. 图片文件名设置 ---
# 请确保这些名字和你 GitHub 仓库里的完全一致（区分大小写）
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 核心逻辑：DNA 动画生成器 ---
def get_dna_animation(methylation_level):
    """
    根据甲基化水平生成不同的 DNA 视觉效果
    使用字符动画模拟双螺旋，兼容性最好
    """
    # 定义颜色
    # 甲基化高 = 红色 (抑制)
    # 甲基化低 = 蓝色 (活跃)
    # 中间状态 = 紫色

    if methylation_level > 66:
        color = "#FF4B4B"  # 红色
        status = "高度甲基化 (抑制)"
        desc = "基因沉默，染色质紧密。"
    elif methylation_level < 33:
        color = "#00E5FF"  # 蓝色
        status = "低甲基化 (活跃)"
        desc = "基因活跃，染色质松散。"
    else:
        color = "#FFA500"  # 橙色/紫色过渡
        status = "部分甲基化"
        desc = "基因表达受到部分调控。"

    # CSS 动画定义 (字符流动效果)
    css_animation = f"""
    <div style="
        font-family: 'Courier New', monospace;
        font-size: 20px;
        font-weight: bold;
        color: {color};
        text-align: center;
        line-height: 1.2;
        letter-spacing: 5px;
        animation: pulse 1.5s infinite ease-in-out;
        text-shadow: 0 0 10px {color};
    ">
        ATCG<br>
        TAGC<br>
        GCTA<br>
        CGAT
    </div>

    <style>
    @keyframes pulse {{
        0% {{ transform: scale(1); opacity: 0.8; }}
        50% {{ transform: scale(1.1); opacity: 1; }}
        100% {{ transform: scale(1); opacity: 0.8; }}
    }}
    </style>
    """
    return css_animation, status, desc

# --- 4. 页面布局 ---

# 标题
st.markdown("<h1 style='text-align: center;'>🧬 DNA 双螺旋甲基化模拟器</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>拖动滑块，观察小鼠毛色与 DNA 状态的动态关联</p >", unsafe_allow_html=True)

st.divider()

# 滑块输入
methylation = st.slider("调节甲基化水平", 0, 100, 50)

# 创建两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🐭 宏观表现：小鼠毛色")

    # 根据滑块值显示不同的小鼠图片
    if methylation > 66:
        st.image(IMG_BLACK, caption="高甲基化：黑色/深色毛色", use_column_width=True)
    elif methylation < 33:
        st.image(IMG_WHITE, caption="低甲基化：白色/浅色毛色", use_column_width=True)
    else:
        st.image(IMG_GRAY, caption="中甲基化：花斑/灰色毛色", use_column_width=True)

with col2:
    st.subheader("🔬 微观分析：DNA 状态")

    # 获取动态 DNA 内容
    dna_html, status_text, desc_text = get_dna_animation(methylation)

    # 显示 DNA 动画
    st.markdown(dna_html, unsafe_allow_html=True)

    # 显示文字状态
    st.markdown(f"**状态：** <span style='color:{dna_html.split("color: ")[1].split(";")[0]}'>● {status_text}</span>", unsafe_allow_html=True)
    st.info(desc_text)

# 底部说明
st.markdown("---")
st.caption("注：本模拟器演示表观遗传学原理。甲基化通常抑制基因表达。")
