import streamlit as st
import random

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA启动子甲基化模拟", layout="centered")

# --- 2. 图片文件名设置 ---
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 核心功能：绘制横向 DNA 结构 ---
def draw_horizontal_dna(level):
    """
    绘制横向 DNA，明确标出启动子区域，并显示甲基化
    """
    # 定义碱基对的颜色
    colors = {
        "A-T": "#FF5252", # 红色
        "T-A": "#448AFF", # 蓝色
        "C-G": "#69F0AE", # 绿色
        "G-C": "#FFD740"  # 黄色
    }
    
    strand_color = "#333333"  # 骨架颜色
    methyl_color = "#FF1744"  # 甲基颜色

    # 设置 DNA 长度
    total_rungs = 12
    methylated_count = int((level / 100) * total_rungs)
    
    # 模拟甲基化位置：特意让甲基化集中在启动子区域（前6个碱基）
    promoter_length = 6 
    methylated_positions = []
    
    if level > 0:
        # 大部分甲基化发生在启动子区域 (0 到 5)
        # 如果甲基化程度高，也会扩散到非启动子区域
        if level <= 50:
             # 低甲基化：只在启动子区域随机
            possible_indices = list(range(promoter_length))
            methylated_positions = random.sample(possible_indices, max(1, methylated_count))
        else:
            # 高甲基化：启动子区域全满，剩下的去后面
            methylated_positions = list(range(promoter_length))
            remaining_count = methylated_count - promoter_length
            if remaining_count > 0:
                possible_indices = list(range(promoter_length, total_rungs))
                # 防止采样数量超过总数
                if remaining_count > len(possible_indices):
                    remaining_count = len(possible_indices)
                methylated_positions.extend(random.sample(possible_indices, remaining_count))

    # --- 开始构建 SVG ---
    width = 700
    height = 200
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">'
    
    # 定义箭头标记（用于指示启动子方向）
    svg += '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="0" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#FF5722" /></marker></defs>'

    # 绘制两条骨架（横线）
    y_top = 60
    y_bottom = 140
    start_x = 50
    end_x = 650
    
    svg += f'<line x1="{start_x}" y1="{y_top}" x2="{end_x}" y2="{y_top}" stroke="{strand_color}" stroke-width="4" />'
    svg += f'<line x1="{start_x}" y1="{y_bottom}" x2="{end_x}" y2="{y_bottom}" stroke="{strand_color}" stroke-width="4" />'
    
    # 计算每个碱基对的间距
    step = (end_x - start_x) / (total_rungs + 1)
    
    # 随机生成碱基序列（只是为了显示，逻辑上不影响颜色）
    bases = ["A-T", "T-A", "C-G", "G-C"]
    
    # 绘制启动子背景框 (前6个碱基)
    promoter_end_x = start_x + (promoter_length + 1) * step
    svg += f'<rect x="{start_x - 10}" y="20" width="{promoter_end_x - start_x + 20}" height="160" fill="#FFF3E0" stroke="#FF5722" stroke-width="2" stroke-dasharray="5,5" rx="10" ry="10" opacity="0.6"/>'
    
    # 添加启动子文字标签
    svg += f'<text x="{start_x + (promoter_length * step)/2}" y="15" font-family="Arial" font-size="16" fill="#E65100" font-weight="bold" text-anchor="middle">启动子区域 (Promoter)</text>'
    svg += f'<text x="{start_x + (promoter_length * step)/2}" y="195" font-family="Arial" font-size="12" fill="#E65100" text-anchor="middle">RNA聚合酶结合位点</text>'
    
    # 绘制碱基对（梯子横杠）和甲基化标记
    for i in range(total_rungs):
        cx = start_x + (i + 1) * step
        base_pair = random.choice(bases)
        color = colors[base_pair]
        
        # 绘制横杠（碱基对）
        svg += f'<line x1="{cx}" y1="{y_top + 5}" x2="{cx}" y2="{y_bottom - 5}" stroke="{color}" stroke-width="8" stroke-linecap="round" />'
        
        # 绘制碱基文字 (白色加粗)
        # 简单处理：只写第一个字母代表上面的链
        base_letter = base_pair.split('-')[0]
        svg += f'<text x="{cx}" y="{y_top - 15}" font-family="Arial" font-size="14" fill="white" font-weight="bold" text-anchor="middle">{base_letter}</text>'

        # 如果有甲基化，画红色圆球和 -CH3
        if i in methylated_positions:
            # 红色圆球
            svg += f'<circle cx="{cx}" cy="{y_top - 15}" r="8" fill="{methyl_color}" stroke="white" stroke-width="2"/>'
            # 文字 CH3
            svg += f'<text x="{cx}" y="{y_top - 10}" font-family="Arial" font-size="10" fill="white" font-weight="bold" text-anchor="middle">CH3</text>'

    # 绘制启动子指示箭头
    svg += f'<line x1="{promoter_end_x}" y1="100" x2="{start_x}" y2="100" stroke="none" marker-end="url(#arrow)" stroke-width="2" />' # 这里的线设为none，只用箭头，或者画一条细线
    # 重新画一条带箭头的线覆盖在背景上，或者就在背景框旁边
    svg += f'<line x1="{start_x - 15}" y1="100" x2="{promoter_end_x - 15}" y2="100" fill="none" stroke="#FF5722" stroke-width="2" marker-end="url(#arrow)" marker-start="url(#arrow)"/>'

    svg += '</svg>'
    return svg

# --- 4. 页面布局 ---
st.title("🧬 DNA 平面结构甲基化模拟 (启动子版)")

# 使用列布局，左边放DNA，右边放小鼠
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. 分子结构变化")
    # 滑块
    level = st.slider("调节甲基化程度", 0, 100, 0)
    
    # 显示 DNA SVG
    st.markdown(draw_horizontal_dna(level), unsafe_allow_html=True)
    
    st.caption("图示说明：黄色虚线框区域为 **启动子**。红色的 `-CH3` 代表甲基化修饰。当启动子区域布满红色标记时，会阻碍 RNA 聚合酶结合。")

with col2:
    st.subheader("2. 宏观表型结果")
    
    # 逻辑判断
    if level > 60: # 阈值设为60，因为重点在启动子
        st.image(IMG_GRAY, caption="表型：基因沉默，小鼠毛色变灰")
        # 结论文字加大加粗
        st.markdown("""
        <div style="background-color: #f44336; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-top: 20px;">
            <h2 style="margin:0;">🚫 转录被抑制</h2>
            <p style="font-size: 20px; margin-top: 10px;">启动子区域被高度甲基化，<br>RNA聚合酶无法结合，基因“关闭”！</p >
        </div>
        """, unsafe_allow_html=True)
    else:
        st.image(IMG_BLACK, caption="表型：基因正常表达，小鼠毛色黑色")
        # 结论文字加大加粗
        st.markdown("""
        <div style="background-color: #4CAF50; padding: 20px; border-radius: 10px; color: white; text-align: center; margin-top: 20px;">
            <h2 style="margin:0;">✅ 基因正常表达</h2>
            <p style="font-size: 20px; margin-top: 10px;">启动子区域低甲基化，<br>RNA聚合酶顺利结合，基因“开启”！</p >
        </div>
        """, unsafe_allow_html=True)

# 底部解释
st.markdown("---")
st.markdown("""
**原理说明：**
1. **启动子区域**：DNA 上的一段特殊序列（图中黄色框），是 RNA 聚合酶结合并启动转录的地方。
2. **甲基化阻碍**：当甲基基团（-CH3）添加在启动子区域的胞嘧啶上时，会改变 DNA 的空间结构或直接阻碍蛋白质结合。
3. **结果**：启动子甲基化程度越高，基因越难被转录，最终导致性状消失（如小鼠毛色变浅）。
""")
