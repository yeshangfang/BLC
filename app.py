import streamlit as st

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA平面结构甲基化模拟", layout="centered")

# --- 2. 图片文件名设置 ---
# 请确保这些名字和你 GitHub 仓库里的完全一致
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 核心功能：绘制平面 DNA 结构 ---
def draw_flat_dna(level):
    """
    根据甲基化水平绘制平面梯子状 DNA
    level: 0-100
    """
    # 计算有多少个甲基基团 (-CH3) 需要显示
    # 我们总共画 8 对碱基对，根据百分比决定显示几个红灯
    total_rungs = 8
    methylated_count = int((level / 100) * total_rungs)
    
    # 颜色设置：甲基化越高，颜色越红（警示）；越低越蓝（正常）
    strand_color = "#2c3e50" # 骨架颜色（深蓝灰）
    rung_color = "#3498db"   # 碱基对颜色（蓝）
    methyl_color = "#e74c3c" # 甲基基团颜色（红）

    # 开始构建 HTML/SVG
    # 使用 SVG 绘制矢量图，保证清晰不失真
    svg_width = 300
    svg_height = 400
    
    html = f'<div style="text-align: center;"><svg width="{svg_width}" height="{svg_height}" style="border:1px solid #ddd; border-radius:10px; background:#f9f9f9;">'
    
    # 1. 绘制两条骨架 (梯子的长边)
    # 左骨架
    html += f'<rect x="50" y="20" width="15" height="360" fill="{strand_color}" rx="5" />'
    # 右骨架
    html += f'<rect x="235" y="20" width="15" height="360" fill="{strand_color}" rx="5" />'
    
    # 标题
    html += '<text x="150" y="390" text-anchor="middle" font-size="14" fill="#555">DNA 双链平面展开图</text>'

    # 2. 绘制碱基对 (梯子的横档) 和 甲基基团
    for i in range(total_rungs):
        # 计算每个横档的 Y 坐标 (从上往下分布)
        y_pos = 50 + i * 40
        
        # 绘制横档 (碱基对)
        html += f'<line x1="65" y1="{y_pos}" x2="235" y2="{y_pos}" stroke="{rung_color}" stroke-width="4" />'
        
        # 绘制碱基文字 (A-T, C-G 随机模拟)
        bases = ["A - T", "C - G", "T - A", "G - C"]
        base_text = bases[i % 4]
        html += f'<text x="150" y="{y_pos}" text-anchor="middle" dominant-baseline="middle" font-size="12" fill="white" font-weight="bold">{base_text}</text>'

        # --- 关键逻辑：如果当前层级需要甲基化，就画 -CH3 ---
        # 我们假设甲基化是从上往下依次发生的
        if i < methylated_count:
            # 绘制甲基基团 (-CH3) - 在右侧骨架外侧
            # 红色圆圈代表甲基
            html += f'<circle cx="265" cy="{y_pos}" r="12" fill="{methyl_color}" />'
            # 文字 -CH3
            html += f'<text x="265" y="{y_pos}" text-anchor="middle" dominant-baseline="middle" font-size="10" fill="white" font-weight="bold">-CH3</text>'
            
            # 画一条线连接碱基对和甲基 (表示结合在碱基上)
            html += f'<line x1="235" y1="{y_pos}" x2="253" y2="{y_pos}" stroke="{methyl_color}" stroke-width="2" stroke-dasharray="2,2" />'

    html += '</svg></div>'
    return html

# --- 4. 页面布局 ---
st.title("🧬 DNA 平面结构甲基化模拟")
st.markdown("观察甲基基团 (-CH3) 如何附着在 DNA 碱基上，从而改变基因表达。")

# 滑块
methylation_level = st.slider("调节甲基化程度", 0, 100, 0, 5)

# 两列布局
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. 分子结构变化")
    # 显示我们刚刚生成的平面 DNA 图
    st.markdown(draw_flat_dna(methylation_level), unsafe_allow_html=True)
    
    if methylation_level > 0:
        st.caption(f"🔴 图中红色圆点代表 **{int(methylation_level/100 * 8)}** 个甲基基团 (-CH3)，它们像锁一样锁住了基因。")
    else:
        st.caption("🟢 当前 DNA 结构纯净，无甲基化修饰，基因处于开放状态。")

with col2:
    st.subheader("2. 宏观表型结果")
    # 逻辑判断
    if methylation_level < 30:
        st.image(IMG_BLACK, caption="基因活跃：黑色毛色", use_column_width=True)
        st.success("结果：基因正常转录，合成黑色素。")
    elif methylation_level < 70:
        st.image(IMG_GRAY, caption="基因减弱：灰色毛色", use_column_width=True)
        st.warning("结果：基因表达受阻，毛色变浅。")
    else:
        st.image(IMG_WHITE, caption="基因沉默：白色毛色", use_column_width=True)
        st.error("结果：基因被关闭，无法合成黑色素。")

# 底部说明
st.divider()
st.markdown("""
**原理说明：**
在平面图中，您可以看到：
1. **两侧竖线**：代表 DNA 的磷酸骨架。
2. **中间横线**：代表碱基对 (A-T, C-G)。
3. **右侧红色 -CH3**：当甲基化发生时，甲基基团会结合在胞嘧啶 (C) 上，物理上阻碍了转录因子的结合，导致基因沉默。
""")
