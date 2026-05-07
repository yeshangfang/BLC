import streamlit as st

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA双螺旋甲基化模拟", layout="centered")

# --- 2. 图片文件名设置 ---
# 请确保上传的文件名与这里一致 (根据你的反馈，小鼠图片是正常的)
IMG_WHITE = "white.png"
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"

# --- 3. 自定义CSS：用于绘制DNA双螺旋 ---
# 这里我们用代码画出双螺旋，而不是用图片，这样更稳定
def local_css():
    st.markdown("""
        <style>
        .dna-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
            margin-bottom: 20px;
            position: relative;
        }
        /* 绘制两条螺旋骨架 */
        .helix {
            border-left: 4px solid #4CAF50;
            border-right: 4px solid #4CAF50;
            height: 100%;
            width: 100px;
            position: relative;
            transform: perspective(500px) rotateY(15deg);
        }
        /* 绘制碱基对（横杠） */
        .rung {
            position: absolute;
            width: 100%;
            height: 4px;
            background-color: #2196F3;
            left: 0;
            transform: translateY(-50%);
            box-shadow: 0 0 5px #2196F3;
        }
        /* 绘制甲基化基团 (红灯) */
        .methyl-group {
            position: absolute;
            width: 12px;
            height: 12px;
            background-color: red;
            border-radius: 50%;
            right: -14px; /* 挂在右侧骨架上 */
            box-shadow: 0 0 8px red;
            opacity: 0; /* 默认隐藏 */
            transition: opacity 0.3s;
        }
        </style>
    """, unsafe_allow_html=True)

def display_dna(level):
    # 根据甲基化程度计算需要显示多少个“红灯”
    # 我们总共画10个碱基对，根据百分比决定显示几个红灯
    num_rungs = 10
    methylated_count = int((level / 100) * num_rungs)

    html_str = '<div class="dna-container"><div class="helix">'

    for i in range(num_rungs):
        # 计算每个横杠的位置 (百分比)
        top_pos = (i + 1) * (100 / (num_rungs + 1))

        # 添加横杠 (碱基对)
        html_str += f'<div class="rung" style="top: {top_pos}%;"></div>'

        # 如果是需要甲基化的部分，添加红灯
        # 这里为了视觉效果
