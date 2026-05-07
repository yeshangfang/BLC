import streamlit as st
import random
from PIL import Image, ImageDraw, ImageEnhance
import io
import os

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
    }
    /* 卡片容器 */
    .card {
        background-color: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #E0E0E0;
    }
    /* 标题样式 */
    h1, h2, h3 {
        color: #333;
        font-weight: 600;
    }
    /* DNA 容器 */
    .dna-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        margin: 20px 0;
    }
    /* 碱基盒子 */
    .base-box {
        width: 40px;
        height: 50px;
        border-radius: 8px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 18px;
        position: relative;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .top-base { color: #E74C3C; } /* 上链红色 */
    .bottom-base { color: #3498DB; } /* 下链蓝色 */
    .label { font-size: 10px; color: #666; margin-top: 4px; font-weight: normal; }
    /* 甲基化标记 */
    .methyl-tag {
        position: absolute;
        top: -22px;
        background-color: #2C3E50;
        color: white;
        font-size: 10px;
        padding: 2px 5px;
        border-radius: 4px;
        font-weight: normal;
    }
    /* 连线 */
    .connector {
        height: 2px;
        background-color: #ccc;
        width: 2px;
        margin: 0 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 侧边栏控制 ---
with st.sidebar:
    st.header("⚙️ 实验参数")
    methylation_level = st.slider("调节启动子甲基化水平", 0, 100, 17)
    st.info("拖动滑块模拟不同环境因素对基因表达的影响")

# --- 5. 主界面布局 ---
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### 🧬 Agouti 基因甲基化模拟")

# --- 6. DNA 可视化部分 ---
st.markdown("<div class='dna-container'>", unsafe_allow_html=True)

# 计算需要显示多少个 CH3 (前7个碱基是启动子区域，只有这里甲基化才有效)
promoter_length = 7
num_methyl = int((methylation_level / 100) * promoter_length)
# 随机选择位置显示甲基化（为了演示效果，这里简化为从左到右依次显示）
methyl_positions = list(range(num_methyl))

for i in range(len(DNA_TOP_SEQUENCE)):
    top_base = DNA_TOP_SEQUENCE[i]
    bottom_base = DNA_BOTTOM_SEQUENCE[i]

    # 判断是否显示甲基化标签
    methyl_tag_html = ""
    # 只有在启动子区域(前7个)才显示甲基化
    if i < promoter_length and i in methyl_positions:
        methyl_tag_html = '<div class="methyl-tag">CH3</div>'

    # 渲染单个碱基对
    st.markdown(f"""
    <div style="text-align:center;">
        <div class="base-box" style="background-color: #FFEAEA;">
            {methyl_tag_html}
            <span class="top-base">{top_base}</span>
            <div class="connector"></div>
            <span class="bottom-base">{bottom_base}</span>
            <div class="label">{'启动子' if i < 7 else '编码区'}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # End DNA Container

st.caption("注：红色字体代表编码链。启动子区域（前7个碱基）甲基化程度越高，基因表达越受抑制。")
st.markdown("</div>", unsafe_allow_html=True) # End Card

# --- 7. 表型观察与逻辑处理 ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("#### 🐭 表型观察")

    # --- 图片处理逻辑 ---
    # 检查图片是否存在
    if os.path.exists("yellow.png"):
        # 打开原始黄色小鼠图片
        base_image = Image.open("yellow.png")

        # 创建一个黑色的遮罩层
        overlay = Image.new('RGBA', base_image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # 根据甲基化水平决定遮罩的不透明度
        # 0% 甲基化 -> 0 透明度 (全黄)
        # 100% 甲基化 -> 180 透明度 (接近全黑)
        alpha = int((methylation_level / 100) * 180)

        # 在遮罩层上画一个半透明的黑色矩形
        draw.rectangle([0, 0, base_image.size[0], base_image.size[1]], fill=(0, 0, 0, alpha))

        # 合并图片
        final_image = Image.alpha_composite(base_image.convert('RGBA'), overlay)

        # 显示图片
        st.image(final_image, caption="", use_column_width=False)
    else:
        # 如果找不到图片，显示占位符
        st.warning("未找到 `yellow.png`，请确保图片文件在同级目录下。")
        st.write("🟡" * 10) # 简单的文本占位

    # 显示文字描述
    if methylation_level < 30:
        st.success("当前表型：**黄色 (肥胖)**")
    elif methylation_level > 70:
        st.success("当前表型：**黑色 (健康)**")
    else:
        st.success("当前表型：**杂色/褐色 (中间型)**")

with col2:
    st.markdown("#### 📝 实验结论")

    # 逻辑判断
    if methylation_level < 30:
        status = "基因活跃表达"
        explanation = "启动子未甲基化，RNA聚合酶顺利结合，Agouti基因持续表达，小鼠呈黄色且肥胖。"
        color = "green"
    elif methylation_level > 70:
        status = "基因沉默 (不表达)"
        explanation = "启动子高度甲基化，阻碍了RNA聚合酶结合，Agouti基因被抑制，小鼠呈黑色且健康。"
        color = "blue"
    else:
        status = "基因表达受抑 (部分)"
        explanation = "启动子部分甲基化，基因表达水平介于两者之间，小鼠毛色呈现过渡色。"
        color = "orange"

    st.markdown(f"""
    <div class="card" style="background-color: #E3F2FD; border-left: 5px solid #{'2ecc71' if color=='green' else 'e67e22' if color=='orange' else '3498db'};">
        <p><strong>当前状态：</strong> <span style="color:{'green' if color=='green' else 'orange' if color=='orange' else 'blue'}; font-weight:bold;">{status}</span></p >
        <hr style="border: 0; border-top: 1px solid #BDBDBD; margin: 10px 0;">
        <p><strong>• 甲基化水平：</strong> {methylation_level}%</p >
        <p><strong>• 解释：</strong> {explanation}</p >
    </div>
    """, unsafe_allow_html=True)

# --- 页脚 ---
st.markdown("<div style='text-align: center; color: #999; margin-top: 50px; font-size: 12px;'>DNA Methylation Simulation v3.0</div>", unsafe_allow_html=True)
