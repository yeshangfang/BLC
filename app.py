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
                if remaining_count > len(possible_indices):
                    remaining_count = len(possible_indices)
                methylated_positions.extend(random.sample(possible_indices, remaining_count))

    # --- 开始构建 SVG ---
    width = 800  
    height = 200
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background-color: #f0f2f6; border-radius: 10px;">'
    
    y_top = 70
    y_bottom = 150
    start_x = 50
    end_x = 750
    
    svg += f'<line x1="{start_x}" y1="{y_top}" x2="{end_x}" y2="{y_top}" stroke="{strand_color}" stroke-width="4" />'
    svg += f'<line x1="{start_x}" y1="{y_bottom}" x2="{end_x}" y2="{y_bottom}" stroke="{strand_color}" stroke-width="4" />'
    
    step = (end_x - start_x) / (total_rungs + 1)
    bases = ["A-T", "T-A", "C-G", "G-C"]
    
    promoter_end_x = start_x + (promoter_length + 1) * step
    svg += f'<rect x="{start_x - 15}" y="30" width="{promoter_end_x - start_x + 30}" height="160" fill="#FFF9C4" stroke="#FBC02D" stroke-width="2" stroke-dasharray="5,5" rx="10" ry="10" opacity="0.8"/>'
    
    svg += f'<text x="{start_x + (promoter_length * step)/2}" y="25" font-family="Arial" font-size="18" fill="#F57F17" font-weight="bold" text-anchor="middle">启动子区域 (Promoter)</text>'
    svg += f'<text x="{start_x + (promoter_length * step)/2}" y="210" font-family="Arial" font-size="14" fill="#F57F17" text-anchor="middle">RNA聚合酶结合位点</text>'
    
    for i in range(total_rungs):
        cx = start_x + (i + 1) * step
        base_pair = random.choice(bases)
        
        top_base = base_pair.split('-')[0]
        svg += f'<text x="{cx}" y="{y_top + 5}" font-family="Arial" font-size="20" fill="{base_text_color}" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{top_base}</text>'
        
        bottom_base = base_pair.split('-')[1]
        svg += f'<text x="{cx}" y="{y_bottom - 5}" font-family="Arial" font-size="20" fill="{base_text_color}" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{bottom_base}</text>'

        if i in methylated_positions:
            svg += f'<circle cx="{cx}" cy="{y_top - 20}" r="12" fill="{methyl_color}" stroke="white" stroke-width="2"/>'
            svg += f'<text x="{cx}" y="{y_top - 15}" font-family="Arial" font-size="12" fill="white" font-weight="bold" text-anchor="middle">CH3</text>'
            svg += f'<line x1="{cx}" y1="{y_top - 8}" x2="{cx}" y2="{y_top + 5}" stroke="{methyl_color}" stroke-width="2" stroke-dasharray="2,2" />'

    svg += '</svg>'
    return svg

# --- 4. 页面布局 ---

st.title("🧬 DNA 平面结构甲基化模拟")

# 使用三列布局，每列占据 1/3
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.subheader("1. 调节甲基化程度")
    # 滑块放在最左边
    level = st.slider("拖动滑块增加甲基化", 0, 100, 0)
    
    # 简单的文字说明
    st.markdown(f"""
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; color: #1565c0; text-align: center; margin-top: 50px;">
        <h3 style="margin:0;">当前数值：{level}%</h3>
        <p style="font-size: 18px; margin-top: 10px;">
        { "高甲基化状态" if level > 60 else "低甲基化状态" }
        </p >
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.subheader("2. 观察分子结构")
    # DNA 图放在中间
    st.markdown(draw_horizontal_dna(level), unsafe_allow_html=True)
    st.caption("图示说明：黄色虚线框区域为 **启动子**。深红色的 `-CH3` 代表甲基化修饰。")

with col3:
    st.subheader("3. 宏观结果与结论")
    # 小鼠和结论放在最右边
    
    # 先显示小鼠图片
    if level > 60: 
        st.image(IMG_GRAY, caption="表型：基因沉默，小鼠毛色变灰/黄")
    else:
        st.image(IMG_BLACK, caption="表型：基因正常表达，小鼠毛色黑色")
    
    # 再显示结论卡片
    if level > 60:
        st.markdown("""
        <div style="background-color: #ffebee; padding: 20px; border-radius: 10px; border: 2px solid #ef5350; color: #c62828; text-align: center; margin-top: 20px;">
            <h3 style="margin:0; font-size: 24px;">🚫 转录被抑制</h3>
            <p style="font-size: 18px; margin-top: 10px; font-weight: bold;">启动子区域被高度甲基化</p >
            <p style="font-size: 16px;">RNA聚合酶无法结合，<br>基因被迫“关闭”！</p >
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border: 2px solid #66bb6a; color: #2e7d32; text-align: center; margin-top: 20px;">
            <h3 style="margin:0; font-size: 24px;">✅ 基因正常表达</h3>
            <p style="font-size: 18px; margin-top: 10px; font-weight: bold;">启动子区域低甲基化</p >
            <p style="font-size: 16px;">RNA聚合酶顺利结合，<br>基因处于“开启”状态！</p >
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
