import streamlit as st
import random

# --- 1. 页面基础设置 ---
st.set_page_config(page_title="横向DNA甲基化模拟器", layout="centered")

# --- 2. 核心逻辑：绘制横向 DNA 结构 ---
def draw_horizontal_dna(methylation_level):
    """
    绘制横向的、彩色碱基对的 DNA 结构图
    并根据甲基化水平添加红色的 CH3 标记
    """
    # 定义碱基对的颜色（鲜艳易区分）
    # A-T: 红色, C-G: 蓝色, T-A: 绿色, G-C: 橙色
    base_colors = ["#FF5252", "#448AFF", "#69F0AE", "#FFD740"]
    strand_color = "#333333"  # 骨架颜色（深灰）
    methyl_color = "#FF1744"  # 甲基基团颜色（亮红）

    # 计算需要显示多少个甲基化位点
    # 这里我们假设 DNA 有 10 个碱基对位点
    total_sites = 10
    methylated_sites = int((methylation_level / 100) * total_sites)

    # 随机生成哪些位点被甲基化（模拟真实情况的不均匀分布）
    # 为了演示效果稳定，这里使用固定种子，实际可改为 random.sample
    random.seed(42)
    methylated_indices = random.sample(range(total_sites), methylated_sites)

    # --- 开始构建 SVG ---
    # 设定画布大小
    width = 600
    height = 250
    padding = 40

    # 计算每个碱基对的间距
    spacing = (width - 2 * padding) / (total_sites - 1)

    svg_content = f'<svg width="{width}" height="{height}" style="background-color: #f9f9f9; border-radius: 10px; border: 1px solid #ddd;">'

    # 1. 绘制两条主链 (磷酸骨架) - 横向
    line_y_top = 80
    line_y_bottom = 170

    # 上链
    svg_content += f'<line x1="{padding}" y1="{line_y_top}" x2="{width-padding}" y2="{line_y_top}" stroke="{strand_color}" stroke-width="8" stroke-linecap="round" />'
    # 下链
    svg_content += f'<line x1="{padding}" y1="{line_y_bottom}" x2="{width-padding}" y2="{line_y_bottom}" stroke="{strand_color}" stroke-width="8" stroke-linecap="round" />'

    # 2. 绘制碱基对 (横档) 和 甲基基团 (CH3)
    for i in range(total_sites):
        x_pos = padding + i * spacing

        # 随机选一个碱基对颜色
        current_color = random.choice(base_colors)

        # 绘制碱基对连线
        svg_content += f'<line x1="{x_pos}" y1="{line_y_top}" x2="{x_pos}" y2="{line_y_bottom}" stroke="{current_color}" stroke-width="4" stroke-dasharray="4,2" />'

        # 绘制碱基小圆点 (增加细节感)
        svg_content += f'<circle cx="{x_pos}" cy="{line_y_top}" r="5" fill="{current_color}" />'
        svg_content += f'<circle cx="{x_pos}" cy="{line_y_bottom}" r="5" fill="{current_color}" />'

        # 如果当前位点在甲基化列表中，绘制 CH3
        if i in methylated_indices:
            # 在上链上方画一个红色的圆点代表甲基
            svg_content += f'<circle cx="{x_pos}" cy="{line_y_top - 25}" r="8" fill="{methyl_color}" stroke="white" stroke-width="2"/>'
            # 写上 CH3 文字
            svg_content += f'<text x="{x_pos}" y="{line_y_top - 28}" font-family="Arial" font-size="10" fill="white" text-anchor="middle" font-weight="bold">CH3</text>'
            # 画一条线连到骨架
            svg_content += f'<line x1="{x_pos}" y1="{line_y_top - 17}" x2="{x_pos}" y2="{line_y_top - 8}" stroke="{methyl_color}" stroke-width="2" />'

    # 3. 添加图例说明 (可选，放在 SVG 内部)
    svg_content += f'<text x="20" y="230" font-family="Arial" font-size="12" fill="#666">注：彩色横档代表不同碱基对，红色圆点代表甲基化位点(-CH3)</text>'

    svg_content += '</svg>'

    return svg_content

# --- 3. 页面布局 ---
st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🧬 DNA 平面结构甲基化模拟器</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #7f8c8d;'>通过滑动滑块，观察横向 DNA 结构中甲基基团的变化</p >", unsafe_allow_html=True)

st.write("---")

# --- 4. 侧边栏/控制区 ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. 设置甲基化水平")
    methylation_level = st.slider("调节甲基化程度 (%)", 0, 100, 0)

    # 根据数值判断状态
    if methylation_level < 30:
        status = "低甲基化 (基因活跃)"
        color_status = "blue"
    elif methylation_level < 70:
        status = "部分甲基化 (基因受抑)"
        color_status = "orange"
    else:
        status = "高甲基化 (基因沉默)"
        color_status = "red"

    st.info(f"当前状态：**{status}**")

# --- 5. 展示区 ---
with col2:
    st.subheader("2. 分子结构可视化")
    # 调用绘图函数
    dna_svg = draw_horizontal_dna(methylation_level)
    # 渲染 HTML
    st.markdown(dna_svg, unsafe_allow_html=True)

st.write("---")
st.markdown("""
**原理说明：**
- **彩色横档**：代表 DNA 的碱基对（A-T, C-G等），不同颜色区分不同碱基。
- **红色 CH3 标记**：代表甲基基团。当滑块数值升高，DNA 骨架上挂载的 CH3 增多。
- **生物学意义**：通常 DNA 甲基化程度越高，基因表达受到的抑制越强。
""")
