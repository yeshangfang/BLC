import streamlit as st

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA甲基化模拟器", layout="centered")

# --- 2. 核心设置：图片文件名 (请严格核对！) ---
# 请去你的 GitHub 仓库里看一眼，图片后缀是 .png 还是 .jpg？文件名中间有空格吗？
# 必须和 GitHub 里的一模一样（区分大小写）！
IMG_WHITE = "white.png"
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"

# --- 3. 美化 DNA 的 CSS 代码 ---
# 我们用代码画一个动态的双螺旋，比图片更清晰，且不会加载失败
st.markdown("""
    <style>
    /* 容器 */
    .dna-scene {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 150px;
        margin: 20px 0;
        perspective: 600px;
    }
    /* 螺旋骨架 */
    .strand {
        position: absolute;
        width: 120px;
        height: 100px;
        border: 3px solid #4CAF50;
        border-radius: 50%;
        border-color: #4CAF50 transparent #4CAF50 transparent;
        animation: spin 2s infinite linear;
        opacity: 0.8;
    }
    .strand:nth-child(2) {
        transform: rotateY(180deg);
        border-color: transparent #FF5722 transparent #FF5722;
    }
    /* 碱基对连接线 */
    .rung {
        position: absolute;
        width: 100px;
        height: 2px;
        background: #ddd;
        top: 50%;
        transform-origin: center;
    }
    /* 动画定义 */
    @keyframes spin {
        0% { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }
    </style>

    <div class="dna-scene">
        <div class="strand"></div>
        <div class="strand"></div>
        <!-- 模拟几条连接线 -->
        <div class="rung" style="transform: rotate(0deg);"></div>
        <div class="rung" style="transform: rotate(30deg);"></div>
        <div class="rung" style="transform: rotate(60deg);"></div>
        <div class="rung" style="transform: rotate(90deg);"></div>
        <div class="rung" style="transform: rotate(120deg);"></div>
        <div class="rung" style="transform: rotate(150deg);"></div>
    </div>
""", unsafe_allow_html=True)

# --- 4. 标题 ---
st.title("🧬 DNA 双螺旋甲基化模拟器")
st.write("通过拖动滑块，观察小鼠毛色的变化以及 DNA 甲基化的程度。")

# --- 5. 滑块控制 ---
methylation_level = st.slider(
    "调节甲基化水平",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)

# --- 6. 逻辑判断与显示 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("宏观表现：小鼠毛色")
    if methylation_level < 30:
        st.image(IMG_BLACK, caption="低甲基化：毛色黑色 (Agouti 基因活跃)")
    elif methylation_level < 70:
        st.image(IMG_GRAY, caption="中等甲基化：毛色灰褐色")
    else:
        st.image(IMG_WHITE, caption="高甲基化：毛色白色 (Agouti 基因沉默)")

with col2:
    st.subheader("微观分析：DNA 状态")
    # 根据滑块数值显示不同的文字描述
    if methylation_level < 30:
        st.markdown("🔴 **状态：基因活跃**")
        st.write("DNA 启动子区域几乎没有甲基化修饰。")
        st.write("转录因子可以顺利结合，Agouti 基因大量表达，导致小鼠呈现黑色。")
    elif methylation_level < 70:
        st.markdown("🟠 **状态：部分抑制**")
        st.write("DNA 上出现了一些甲基化标记。")
        st.write("基因表达受到部分阻碍，毛色呈现中间态。")
    else:
        st.markdown("🟢 **状态：基因沉默**")
        st.write("DNA 启动子区域高度甲基化。")
        st.write("转录机器无法结合，Agouti 基因被关闭，小鼠恢复野生型白色。")
