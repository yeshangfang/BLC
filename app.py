import streamlit as st
import random
import time

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA启动子甲基化模拟", layout="centered")

# 自定义CSS以优化布局间距和字体
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
    }
    .stMarkdown h3 {
        margin-top: 0;
    }
    /* 增加底部容器的内边距 */
    .bottom-container {
        padding-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 图片文件名设置 ---
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 核心功能：绘制横向 DNA 结构 ---
def draw_horizontal_dna(level):
    """
    绘制横向 DNA 结构
    """
    base_text_color = "#455A64"
    strand_color = "#333333"
    methyl_color = "#D50000"

    total_rungs = 14
    methylated_count = int((level / 100) * total_rungs)

    promoter_length = 7
    methylated_positions = []

    if level > 0:
        if level <= 60:
            possible_indices = list(range(promoter_length))
            methylated_positions = random.sample(possible_indices, max(1, methylated_count))
        else:
            methylated_positions = list(range(promoter_length))
            remaining_count = methylated_count - promoter_length
            if remaining_count > 0:
                possible_indices = list(range(promoter_length, total_rungs))
                methylated_positions += random.sample(possible_indices, min(remaining_count, len(possible_indices)))

    # 碱基对序列 (14对)
    bases_top = ['T', 'A', 'C', 'G', 'A', 'T', 'C', 'G', 'A', 'T', 'A', 'C', 'G', 'T']
    bases_bottom = ['A', 'T', 'G', 'C', 'T', 'A', 'G', 'C', 'T', 'A', 'T', 'G', 'C', 'A']

    # 计算 SVG 尺寸 (加宽)
    rung_spacing = 40
    width = 620
    height = 160
    start_x = 40
    y_top = 50
    y_bottom = 100

    svg_content = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'

    # 绘制主链 (两条长线)
    svg_content += f'<line x1="{start_x}" y1="{y_top}" x2="{width-20}" y2="{y_top}" stroke="{strand_color}" stroke-width="3" stroke-linecap="round"/>'
    svg_content += f'<line x1="{start_x}" y1="{y_bottom}" x2="{width-20}" y2="{y_bottom}" stroke="{strand_color}" stroke-width="3" stroke-linecap="round"/>'

    # 绘制横档 (碱基对和甲基化标记)
    for i in range(total_rungs):
        x = start_x + (i * rung_spacing) + 10

        # 绘制连接线
        line_color = base_text_color
        svg_content += f'<line x1="{x}" y1="{y_top}" x2="{x}" y2="{y_bottom}" stroke="{line_color}" stroke-width="1.5" stroke-dasharray="2,2"/>'

        # 绘制碱基文字
        svg_content += f'<text x="{x}" y="{y_top-10}" fill="{base_text_color}" font-size="16" text-anchor="middle" font-family="Arial">{bases_top[i]}</text>'
        svg_content += f'<text x="{x}" y="{y_bottom+20}" fill="{base_text_color}" font-size="16" text-anchor="middle" font-family="Arial">{bases_bottom[i]}</text>'

        # 绘制甲基化标记 (红色圆点) - 只在上链显示
        if i in methylated_positions:
            svg_content += f'<circle cx="{x}" cy="{y_top-15}" r="6" fill="{methyl_color}" />'

    svg_content += '</svg>'
    return svg_content

# --- 4. 主程序布局 ---

# 标题
st.title("🧬 DNA 平面结构甲基化模拟")

# ==========================================
# 第一部分：滑块模块 (占据顶部 1/3 区域)
# ==========================================
st.subheader("1. 调节甲基化程度")
col_slider_1, col_slider_2, col_slider_3 = st.columns([1, 6, 1])
with col_slider_2:
    methylation_level = st.slider(
        "拖动滑块以改变甲基化水平",
        min_value=0,
        max_value=100,
        value=0,
        step=1
    )

    # 显示当前数值状态
    if methylation_level < 30:
        status_text = "低甲基化状态 (基因活跃)"
        status_color = "green"
    elif methylation_level < 70:
        status_text = "中等甲基化状态"
        status_color = "orange"
    else:
        status_text = "高甲基化状态 (基因沉默)"
        status_color = "red"

    st.markdown(f"""
    <div style="
        background-color: #e0e0e0;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
        border: 1px solid #ccc;
    ">
        <h4 style="margin:0; color:#333;">当前数值: <span style="color:{status_color};">{methylation_level}%</span></h4>
        <p style="margin:5px 0 0 0; font-size: 14px; color: #555;">{status_text}</p >
    </div>
    """, unsafe_allow_html=True)

st.markdown("---") # 分割线

# ==========================================
# 第二部分：DNA 结构模块 (占据中间 1/3 区域)
# ==========================================
st.subheader("2. 观察分子结构")

# 居中显示 DNA
col_dna_1, col_dna_2, col_dna_3 = st.columns([1, 8, 1])
with col_dna_2:
    st.markdown(
        "<div style='text-align: center; background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>",
        unsafe_allow_html=True
    )
    st.markdown("**启动子区域 (Promoter)**")
    # 调用绘图函数
    st.markdown(draw_horizontal_dna(methylation_level), unsafe_allow_html=True)
    st.caption("注：红色圆点代表甲基化修饰，主要集中在启动子区域（前7个碱基）。")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---") # 分割线

# ==========================================
# 第三部分：小鼠与结论 (占据底部 1/3 区域)
# ==========================================
st.subheader("3. 宏观结果与结论")

# 创建左右两列
col_left, col_right = st.columns([1, 1]) # 1:1 比例

with col_left:
    st.markdown("#### 实验对象 (小鼠)")
    # 根据甲基化水平选择图片
    if methylation_level > 60:
        img_path = IMG_BLACK
        mouse_desc = "表型：**黑色** (Agouti基因沉默)"
    elif methylation_level < 30:
        img_path = IMG_WHITE # 假设白色代表黄色/肥胖表型，或者用灰色
        mouse_desc = "表型：**黄色/肥胖** (Agouti基因过表达)"
    else:
        img_path = IMG_GRAY
        mouse_desc = "表型：**灰色/杂色** (混合状态)"

    # 尝试显示图片，如果不存在则显示占位符
    try:
        st.image(img_path, caption=f"当前表型: {mouse_desc}", use_column_width=True)
    except Exception as e:
        st.warning("图片未找到，请确保 gray.png, black.png, white.png 在同级目录。")
        st.write(f"**{mouse_desc}**")

with col_right:
    st.markdown("#### 结论分析")

    # 结论框逻辑
    if methylation_level > 60:
        st.success("""
        **✅ 基因表达被抑制**
        - **机制**：启动子区域高度甲基化。
        - **结果**：阻碍了转录因子的结合，基因关闭。
        - **表型**：小鼠呈现健康体型（黑色）。
        """)
    elif methylation_level < 30:
        st.error("""
        **❌ 基因过度表达**
        - **机制**：启动子区域低甲基化。
        - **结果**：转录因子自由结合，基因持续开启。
        - **表型**：小鼠呈现黄色且肥胖。
        """)
    else:
        st.info("""
        **⚖️ 基因表达中等**
        - **机制**：部分甲基化。
        - **结果**：基因表达水平介于两者之间。
        - **表型**：小鼠呈现杂色（灰/黄相间）。
        """)

# 底部版权或说明
st.markdown("<br><br><center style='color: #888;'>DNA甲基化教学演示程序</center>", unsafe_allow_html=True)
