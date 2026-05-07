import streamlit as st

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA甲基化模拟器", layout="centered")

# --- 2. 核心设置：图片文件名 ---
# 既然你的小鼠图片正常，说明这两个文件名是对的，保持不动即可
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 注入美观的 DNA 双螺旋 CSS 动画 ---
# 这里我们用代码画一个旋转的双螺旋，替代原来的静态圆圈
st.markdown("""
    <style>
    /* DNA 容器 */
    .dna-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 120px;
        margin-bottom: 10px;
        perspective: 800px; /* 3D 透视感 */
    }
    /* 螺旋轨道通用样式 */
    .helix {
        position: absolute;
        width: 100px;
        height: 100px;
        border: 4px solid #4CAF50; /* 绿色轨道 */
        border-radius: 50%;
        opacity: 0.8;
        box-shadow: 0 0 10px #4CAF50;
    }
    /* 左边轨道 */
    .left-strand {
        animation: spin-left 2s infinite linear;
        border-right-color: transparent; /* 制造螺旋缺口感 */
    }
    /* 右边轨道 */
    .right-strand {
        animation: spin-right 2s infinite linear;
        border-left-color: transparent;
    }
    /* 中间的横杠（碱基对） */
    .rung {
        position: absolute;
        width: 100px;
        height: 4px;
        background: #81C784;
        top: 50%;
        transform: translateY(-50%) rotateX(70deg);
        box-shadow: 0 0 5px #81C784;
    }
    /* 动画定义 */
    @keyframes spin-left {
        0% { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }
    @keyframes spin-right {
        0% { transform: rotateY(180deg); }
        100% { transform: rotateY(540deg); }
    }
    </style>

    <!-- HTML 结构：两个旋转的圈 + 中间横杠 -->
    <div class="dna-container">
        <div class="helix left-strand"></div>
        <div class="helix right-strand"></div>
        <div class="rung"></div>
    </div>
""", unsafe_allow_html=True)

# --- 4. 标题 ---
st.title("🧬 DNA 双螺旋甲基化模拟器")
st.write("通过拖动滑块，观察小鼠毛色的变化以及 DNA 甲基化的程度。")

# --- 5. 滑块控制 ---
methylation_level = st.slider("调节甲基化水平", 0, 100, 50)

# --- 6. 逻辑判断与显示 ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("宏观表现：小鼠毛色")
    if methylation_level > 66:
        st.image(IMG_BLACK, caption="高甲基化：毛色黑色", width=250)
        status = "高度抑制"
        desc = "基因表达被强力阻断，毛色呈现深黑色。"
    elif methylation_level < 33:
        st.image(IMG_WHITE, caption="低甲基化：毛色黄色", width=250)
        status = "活跃表达"
        desc = "基因正常表达，毛色呈现亮黄色。"
    else:
        st.image(IMG_GRAY, caption="中甲基化：毛色灰褐色", width=250)
        status = "部分抑制"
        desc = "基因表达受到部分阻碍，毛色呈现中间态。"

with col2:
    st.subheader("微观分析：DNA 状态")
    # 这里我们不再显示图片，而是用文字和状态点来描述
    st.markdown(f"### 状态：**{status}**")
    st.write(desc)

    # 简单的视觉条
    st.progress(methylation_level)
