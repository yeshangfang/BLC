import streamlit as st

# --- 1. 页面配置 ---
st.set_page_config(page_title="Agouti基因甲基化模拟", layout="centered", initial_sidebar_state="collapsed")

# --- 2. 核心设定：固定DNA序列 (人教版标准) ---
# 上链序列固定，不再随机
DNA_TOP_SEQUENCE = "ATGCAGTCGATCGA"

def get_complement(base):
    """严格互补配对：A-T, C-G"""
    pairs = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return pairs.get(base, '')

# 自动生成下链
DNA_BOTTOM_SEQUENCE = "".join([get_complement(b) for b in DNA_TOP_SEQUENCE])

# --- 3. 样式设置 ---
st.markdown("""
    <style>
    /* 全局字体与背景 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    body {
        background-color: #F7F9FA;
        font-family: 'Inter', sans-serif;
        color: #2C3E50;
    }
    /* 隐藏默认菜单 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 居中图片容器 */
    .mouse-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 4. 核心功能：绘制DNA结构 ---
def draw_dna_structure(methylation_level):
    # 莫兰迪配色
    PROMOTER_BG = "#D5E1DF"  # 启动子背景
    CODING_BG = "#D6E2E9"    # 编码区背景
    METHYL_COLOR = "#E07A5F" # 甲基化标记颜色
    TEXT_COLOR = "#3D405B"   # 文字颜色
    STRAND_COLOR = "#81B29A" # 骨架颜色

    total_rungs = 14
    promoter_length = 7  # 启动子区域长度（前7个碱基）
    
    # 计算甲基化数量
    methylated_count = int((methylation_level / 100) * promoter_length)
    
    # 随机选择甲基化位置（仅在启动子区域）
    methylated_positions = []
    if level > 0:
        possible_indices = list(range(promoter_length))
        # 保证至少有一个或者全选
        count = max(1, methylated_count) if methylation_level < 100 else promoter_length
        methylated_positions = random.sample(possible_indices, min(count, len(possible_indices)))

    # SVG 绘图
    width = 850
    height = 240
    svg = f'<svg width="100%" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" style="filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.1)); border-radius: 12px;">'
    
    # 背景区域
    svg += f'<rect x="20" y="20" width="400" height="200" fill="{PROMOTER_BG}" rx="10" ry="10" opacity="0.6"/>'
    svg += f'<rect x="430" y="20" width="400" height="200" fill="{CODING_BG}" rx="10" ry="10" opacity="0.6"/>'
    
    # 文字标签
    svg += f'<text x="220" y="50" text-anchor="middle" fill="{TEXT_COLOR}" font-size="14" font-weight="bold">启动子区域 (Promoter)</text>'
    svg += f'<text x="630" y="50" text-anchor="middle" fill="{TEXT_COLOR}" font-size="14" font-weight="bold">编码区域 (Coding)</text>'

    # 绘制骨架
    y_top = 100
    y_bottom = 160
    start_x = 50
    end_x = 800
    
    svg += f'<path d="M {start_x} {y_top} Q 425 {y_top-10} 800 {y_top}" fill="none" stroke="{STRAND_COLOR}" stroke-width="6" stroke-linecap="round"/>'
    svg += f'<path d="M {start_x} {y_bottom} Q 425 {y_bottom+10} 800 {y_bottom}" fill="none" stroke="{STRAND_COLOR}" stroke-width="6" stroke-linecap="round"/>'

    # 绘制碱基对
    step = (end_x - start_x) / (total_rungs + 1)

    for i in range(total_rungs):
        cx = start_x + (i + 1) * step
        base_top = DNA_TOP_SEQUENCE[i]
        base_bottom = DNA_BOTTOM_SEQUENCE[i]
        
        # 氢键
        svg += f'<line x1="{cx}" y1="{y_top+15}" x2="{cx}" y2="{y_bottom-15}" stroke="#F2F2F2" stroke-width="2" stroke-dasharray="4,4"/>'
        
        # 上链碱基
        svg += f'<text x="{cx}" y="{y_top}" text-anchor="middle" fill="{TEXT_COLOR}" font-size="18" font-weight="bold">{base_top}</text>'
        # 下链碱基
        svg += f'<text x="{cx}" y="{y_bottom+25}" text-anchor="middle" fill="{TEXT_COLOR}" font-size="18" font-weight="bold">{base_bottom}</text>'

        # 甲基化标记 (CH3 文字)
        if i in methylated_positions:
            # 连接线
            svg += f'<line x1="{cx}" y1="{y_top-15}" x2="{cx}" y2="{y_top-5}" stroke="{METHYL_COLOR}" stroke-width="2"/>'
            # CH3 文字背景圆（为了清晰可见）
            svg += f'<circle cx="{cx}" cy="{y_top-25}" r="12" fill="white" fill-opacity="0.9"/>'
            # CH3 文字
            svg += f'<text x="{cx}" y="{y_top-20}" text-anchor="middle" fill="{METHYL_COLOR}" font-size="10" font-weight="bold">CH3</text>'

    svg += '</svg>'
    return svg

# --- 5. 主程序布局 ---

st.title("🧬 表观遗传学模拟：Agouti 基因")

# --- 控制区 ---
col_ctrl_1, col_ctrl_2 = st.columns([1, 4])
with col_ctrl_1:
    st.markdown("### 实验参数")
with col_ctrl_2:
    level = st.slider("调节启动子甲基化水平", 0, 100, 0, label_visibility="collapsed")

# 状态判断
if level < 30:
    status_text = "低甲基化 (基因活跃)"
    status_color = "#E07A5F" # 红
elif level < 70:
    status_text = "中等甲基化 (基因部分抑制)"
    status_color = "#F2CC8F" # 黄
else:
    status_text = "高甲基化 (基因沉默)"
    status_color = "#81B29A" # 绿

st.markdown(f"""
<div style="text-align: center; margin-top: -20px; margin-bottom: 10px;">
    <span style="color: {status_color}; font-weight: bold; font-size: 1.1em;">● {status_text}</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- 结构观察区 ---
st.markdown("### 分子结构观察 (Agouti 基因启动子区)")
with st.container():
    st.markdown(draw_dna_structure(level), unsafe_allow_html=True)
    st.caption("注：启动子区域的 CH3 标记越多，基因表达越受抑制。")

# --- 结果与表型区 ---
st.markdown("### 表型观察与结论")

# 计算毛色深浅 (0 = 全黄, 1 = 全黑)
# 我们使用一个透明度滤镜来模拟颜色深浅
darkness = level / 100.0 

col_res_1, col_res_2 = st.columns([1, 1.5])

with col_res_1:
    st.markdown("#### 宏观表型")
    
    # 图片逻辑
    # 这里默认使用 yellow_mouse.png。如果文件不存在，会显示一个占位符
    image_path = "yellow_mouse.png" 
    
    # 使用CSS滤镜改变图片颜色深浅
    # brightness(100%) 是原图，brightness(20%) 是很暗（接近黑）
    # 我们混合了 brightness 和 sepia(褐色) 来模拟从黄到黑的过渡
    brightness_val = 100 - (darkness * 80) # 最暗降到20%亮度
    contrast_val = 100 + (darkness * 50)   # 增加一点对比度
    
    filter_style = f"filter: brightness({brightness_val}%) contrast({contrast_val}%) grayscale({darkness * 0.3}); border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"
    
    try:
        # 读取图片二进制数据以应用样式
        with open(image_path, "rb") as f:
            img_data = f.read()
            import base64
            b64 = base64.b64encode(img_data).decode()
            img_html = f'< img src="data:image/png;base64,{b64}" style="{filter_style}" width="250px">'
            st.markdown(f'<div class="mouse-container">{img_html}</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        # 如果没有图片，显示一个带颜色的方块代替（防止报错）
        st.warning(f"未找到图片 '{image_path}'，请确保图片在同级目录下。")
        st.markdown(f"""
        <div class="mouse-container">
            <div style="width:200px; height:150px; background:linear-gradient(135deg, #F2CC8F, #2C3E50 {darkness*100}%); border-radius:15px; display:flex; justify-content:center; align-items:center; color:white; font-weight:bold;">
                小鼠模拟图
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_res_2:
    st.markdown("#### 实验结论")
    if level > 70:
        st.success(f"""
        **表型：黑色 (健康)**
        - **基因状态**：启动子高度甲基化，Agouti 基因**沉默**。
        - **机理**：甲基化修饰阻碍了转录因子的结合，基因无法正常表达。
        """)
    elif level < 30:
        st.error(f"""
        **表型：黄色 (肥胖)**
        - **基因状态**：启动子低甲基化，Agouti 基因**持续表达**。
        - **机理**：基因活跃转录，导致毛色变黄且易肥胖。
        """)
    else:
        st.info(f"""
        **表型：介于黄黑之间**
        - **基因状态**：部分甲基化，基因表达受到**部分抑制**。
        - **机理**：体现了表观遗传修饰对性状的连续调控作用。
        """)

st.markdown("---")
st.markdown("<div style='text-align: center; color: #95A5A6; font-size: 0.8em;'>参考教材：人教版高中生物必修二</div>", unsafe_allow_html=True)
