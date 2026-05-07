import streamlit as st
import random

# --- 1. 页面配置 ---
st.set_page_config(page_title="Agouti基因甲基化模拟", layout="centered")

# --- 2. 核心数据与逻辑 ---
# 预设固定的 DNA 序列 (上链)，确保科学准确性
# 前7个为启动子区域，后7个为编码区域
FIXED_DNA_TOP = ['A', 'T', 'G', 'C', 'A', 'G', 'T', 'C', 'G', 'A', 'T', 'C', 'G', 'A']
# 根据互补配对原则生成的下链 (A-T, C-G)
FIXED_DNA_BOTTOM = ['T', 'A', 'C', 'G', 'T', 'C', 'A', 'G', 'C', 'T', 'A', 'G', 'C', 'T']

def get_mouse_info(level):
    """根据甲基化程度返回小鼠信息"""
    if level > 60:
        # 高甲基化：白色/淡黄色，肥胖
        return "🐁", "棕黄色 (肥胖)", "#FFFDD0", "基因被沉默，Agouti蛋白不表达"
    elif level > 30:
        # 中甲基化：斑驳色/灰色
        return "🐁", "斑驳色 (中等)", "#D3D3D3", "基因部分表达，毛色花白"
    else:
        # 低甲基化：黑色，健康
        return "🐭", "黑色 (健康)", "#2F4F4F", "基因正常表达，Agouti蛋白高表达"

# --- 3. 界面绘制 ---

# 自定义CSS：美化布局
st.markdown("""
    <style>
    /* 全局字体 */
    html, body, [class*="css"] {
        font-family: 'Microsoft YaHei', sans-serif;
    }
    /* 紧凑布局 */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 800px;
    }
    /* 标题样式 */
    h2, h3 {
        color: #2C3E50;
        font-weight: 600;
    }
    /* DNA碱基样式 */
    .base {
        display: inline-block;
        width: 30px;
        height: 30px;
        line-height: 30px;
        text-align: center;
        border-radius: 4px;
        font-weight: bold;
        margin: 0 2px;
        font-size: 14px;
    }
    .base-A { background-color: #FFEBEE; color: #C62828; } /* A - 红 */
    .base-T { background-color: #E8F5E9; color: #2E7D32; } /* T - 绿 */
    .base-C { background-color: #E3F2FD; color: #1565C0; } /* C - 蓝 */
    .base-G { background-color: #FFF8E1; color: #F9A825; } /* G - 黄 */

    /* 甲基化标记 */
    .methyl-tag {
        font-size: 12px;
        color: #D32F2F;
        font-weight: bold;
        margin-bottom: 2px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 主程序 ---

# 1. 标题
st.markdown("<h2 style='text-align: center;'>🧬 表观遗传学模拟：Agouti 基因</h2>", unsafe_allow_html=True)

# 2. 侧边栏/控制区 (放在顶部)
st.markdown("### ⚙️ 实验参数设置")
col1, col2 = st.columns([1, 3])
with col1:
    st.write("甲基化程度")
with col2:
    methylation_level = st.slider("调节启动子甲基化水平", 0, 100, 50)

# 计算当前状态
mouse_icon, mouse_text, mouse_color, conclusion_text = get_mouse_info(methylation_level)

# 3. 分子结构观察区
st.markdown("---")
st.markdown("### 🧬 分子结构观察 (Agouti 基因启动子区)")

# 绘制 DNA
# 使用列布局来对齐上下链
cols = st.columns(14) # 14个碱基

for i in range(14):
    with cols[i]:
        # 判断是否需要显示甲基化标记 (仅在启动子区域 0-6)
        is_methylated = False
        if i < 7: # 启动子区域
            # 根据滑块数值，按比例决定哪些位置甲基化
            # 简单逻辑：如果随机数小于甲基化比例，则甲基化
            # 为了演示稳定，我们假设前 N 个被甲基化
            threshold = (methylation_level / 100) * 7
            if i < threshold:
                is_methylated = True

        # 绘制甲基化标记
        if is_methylated:
            st.markdown(f"<div class='methyl-tag'>● Me</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True) # 占位

        # 绘制上链碱基
        base_top = FIXED_DNA_TOP[i]
        st.markdown(f"<div class='base base-{base_top}'>{base_top}</div>", unsafe_allow_html=True)

        # 绘制下链碱基
        base_bottom = FIXED_DNA_BOTTOM[i]
        st.markdown(f"<div class='base base-{base_bottom}'>{base_bottom}</div>", unsafe_allow_html=True)

# 区域标注
st.markdown("""
    <div style='margin-top: 10px; font-size: 12px; color: #666; display: flex; justify-content: space-between; padding: 0 10px;'>
        <span>⬅️ 启动子区域 (调控开关)</span>
        <span>编码区域 (基因主体) ➡️</span>
    </div>
""", unsafe_allow_html=True)

# 4. 表型与结论区
st.markdown("---")
col_res1, col_res2 = st.columns([1, 2])

with col_res1:
    st.markdown("### 🐭 表型观察")
    st.markdown(f"<h1 style='text-align: center; margin-top: 20px;'>{mouse_icon}</h1>", unsafe_allow_html=True)
    st.markdown(f"**颜色：** <span style='color:{mouse_color};'>■ {mouse_text}</span>", unsafe_allow_html=True)

with col_res2:
    st.markdown("### 📝 实验结论")
    st.info(f"**当前状态：** 启动子甲基化水平为 **{methylation_level}%**。\n\n**结论：** {conclusion_text}")

# 底部说明
st.markdown("<div style='margin-top: 20px; font-size: 12px; color: #999; text-align: center;'>注：DNA序列本身未发生改变，改变的仅是启动子区域的甲基化修饰。</div>", unsafe_allow_html=True)
