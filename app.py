import streamlit as st
import random

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA启动子甲基化模拟", layout="wide")

# --- 2. 图片文件名设置 ---
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"

# --- 3. 核心功能：绘制横向 DNA 结构 ---
def draw_horizontal_dna(level):
    """
    绘制横向 DNA 结构
    - 碱基对直接用字母表示，不再使用彩色横杠
    - 甲基化颜色调整为更明显的亮红色
    """
    # 定义碱基对的颜色 - 统一使用深灰色，不再凸显颜色
    base_text_color = "#455A64" 
    
    strand_color = "#333333"  # 骨架颜色
    methyl_color = "#D50000"  # 甲基颜色：调整为更深、更刺眼的深红色

    # 设置 DNA 长度
    total_rungs = 14 
    methylated_count = int((level / 100) * total_rungs)
    
    # 模拟甲基化位置：优先集中在启动子区域
    promoter_length = 7 
    methylated_positions = []
    
    if level > 0:
        # 算法：优先填满启动子区域
        if level <= 60:
             # 中低甲基化：主要在启动子区域随机
            possible_indices = list(range(promoter_length))
            methylated_positions = random.sample(possible_indices, max(1, methylated_count))
        else:
            # 高甲基化：启动子全满，剩下的去后面
            methylated_positions = list(range(promoter_length))
            remaining_count = methylated_count - promoter_length
            if remaining_count > 0:
                possible_indices = list(range(promoter_length, total_rungs))
                if remaining_count > len(possible_indices):
                    remaining_count = len(possible_indices)
                methylated_positions.extend(random.sample(possible_indices, remaining_count))

    # --- 开始构建 SVG ---
    width = 900  
    height = 220
    # 背景色保持统一
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background-color: #f0f2f6; border-radius: 10px;">'
    
    # 绘制两条骨架（横线）
    y_top = 70
    y_bottom = 150
    start_x = 50
    end_x = 850
    
    svg += f'<line x1="{start_x}" y1="{y_top}" x2="{end_x}" y2="{y_top}" stroke="{strand_color}" stroke-width="4" />'
    svg += f'<line x1="{start_x}" y1="{y_bottom}" x2="{end_x}" y2="{y_bottom}" stroke="{strand_color}" stroke-width="4" />'
    
    # 计算每个碱基对的间距
    step = (end_x - start_x) / (total_rungs + 1)
    
    # 碱基对序列 (为了视觉丰富，随机生成)
    bases = ["A-T", "T-A", "C-G", "G-C"]
    
    # 绘制启动子背景框
    promoter_end_x = start_x + (promoter_length + 1) * step
    svg += f'<rect x="{start_x - 15}" y="30" width="{promoter_end_x - start_x + 30}" height="160" fill="#FFF9C4" stroke="#FBC02D" stroke-width="2" stroke-dasharray="5,5" rx="10" ry="10" opacity="0.8"/>'
    
    # 添加启动子文字标签
    svg += f'<text x="{start_x + (promoter_length * step)/2}" y="25" font-family="Arial" font-size="18" fill="#F57F17" font-weight="bold" text-anchor="middle">启动子区域 (Promoter)</text>'
    svg += f'<text x="{start_x + (promoter_length * step)/2}" y="210" font-family="Arial" font-size="14" fill="#F57F17" text-anchor="middle">RNA聚合酶结合位点</text>'
    
    # 绘制碱基对和甲基化标记
    for i in range(total_rungs):
        cx = start_x + (i + 1) * step
        base_pair = random.choice(bases)
        
        # 不再绘制彩色横杠，只绘制字母
        # 上链字母
        top_base = base_pair.split('-')[0]
        svg += f'<text x="{cx}" y="{y_top + 5}" font-family="Arial" font-size="20" fill="{base_text_color}" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{top_base}</text>'
        
        # 下链字母
        bottom_base = base_pair.split('-')[1]
        svg += f'<text x="{cx}" y="{y_bottom - 5}" font-family="Arial" font-size="20" fill="{base_text_color}" font-weight="bold" text-anchor="middle" dominant-baseline="middle">{bottom_base}</text>'

        # 如果有甲基化，画红色圆球和 -CH3
        if i in methylated_positions:
            # 红色圆球 (颜色更明显)
            svg += f'<circle cx="{cx}" cy="{y_top - 20}" r="12" fill="{methyl_color}" stroke="white" stroke-width="2"/>'
            # 文字 CH3
            svg += f'<text x="{cx}" y="{y_top - 15}" font-family="Arial" font-size="12" fill="white" font-weight="bold" text-anchor="middle">CH3</text>'
            
            # 增加一条连接线，表示甲基结合在碱基上
            svg += f'<line x1="{cx}" y1="{y_top - 8}" x2="{cx}" y2="{y_top + 5}" stroke="{methyl_color}" stroke-width="2" stroke-dasharray="2,2" />'

    svg += '</svg>'
    return svg

# --- 4. 页面布局 ---

# 1. 顶部：滑块控制
st.title("🧬 DNA 平面结构甲基化模拟")
st.markdown("#### 第一步：调节甲基化程度")
level = st.slider("拖动滑块增加甲基化", 0, 100, 0)

st.divider()

# 2. 中间：DNA 结构展示
st.markdown("#### 第二步：观察分子结构变化")
# 居中显示 DNA 图
col_dna, _ = st.columns([2, 1])
with col_dna:
    st.markdown(draw_horizontal_dna(level), unsafe_allow_html=True)
    st.caption("图示说明：黄色虚线框区域为 **启动子**。深红色的 `-CH3` 代表甲基化修饰。")

st.divider()

# 3. 底部：小鼠与结论
st.markdown("#### 第三步：查看宏观结果")
col_mouse, col_conclusion = st.columns([1, 1])

with col_mouse:
    st.subheader("小鼠表现")
    # 逻辑判断
    if level > 60: 
        st.image(IMG_GRAY, caption="表型：基因沉默，小鼠毛色变灰/黄")
    else:
        st.image(IMG_BLACK, caption="表型：基因正常表达，小鼠毛色黑色")

with col_conclusion:
    st.subheader("实验结论")
    # 结论文字加大加粗
    if level > 60:
        st.markdown("""
        <div style="background-color: #ffebee; padding: 30px; border-radius: 15px; border: 2px solid #ef5350; color: #c62828; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <h1 style="margin:0; font-size: 32px;">🚫 转录被抑制</h1>
            <p style="font-size: 24px; margin-top: 15px; font-weight: bold;">启动子区域被高度甲基化</p >
            <p style="font-size: 20px;">RNA聚合酶无法结合，<br>基因被迫“关闭”！</p >
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background-color: #e8f5e9; padding: 30px; border-radius: 15px; border: 2px solid #66bb6a; color: #2e7d32; text-align: center; height: 100%; display: flex; flex-direction: column; justify-content: center;">
            <h1 style="margin:0; font-size: 32px;">✅ 基因正常表达</h1>
            <p style="font-size: 24px; margin-top: 15px; font-weight: bold;">启动子区域低甲基化</p >
            <p style="font-size: 20px;">RNA聚合酶顺利结合，<br>基因处于“开启”状态！</p >
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
