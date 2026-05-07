import streamlit as st
import math

# --- 1. 页面设置 ---
st.set_page_config(page_title="DNA双螺旋甲基化模拟", layout="centered")

# --- 2. 图片文件名设置 ---
# 请确保上传的文件名与这里一致
IMG_WHITE = "white.png"
IMG_GRAY = "gray.png"
IMG_BLACK = "black.png"

# --- 3. 侧边栏 ---
st.sidebar.header("🧬 实验控制台")
st.sidebar.write("拖动滑块，观察甲基化如何改变DNA结构并影响表型。")

# --- 4. 主界面 ---
st.title("DNA 双螺旋甲基化模拟器")
st.markdown("---")

# --- 5. 核心交互 ---
methylation_level = st.slider(
    "🧪 调节 DNA 甲基化程度",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

# --- 6. 逻辑判断 (小鼠表型) ---
if methylation_level < 30:
    mouse_img = IMG_BLACK
    mouse_status = "黑色 (基因活跃)"
    gene_activity = "高表达"
elif 30 <= methylation_level < 70:
    mouse_img = IMG_GRAY
    mouse_status = "灰色 (基因抑制)"
    gene_activity = "中等表达"
else:
    mouse_img = IMG_WHITE
    mouse_status = "白色 (基因沉默)"
    gene_activity = "停止表达"

# --- 7. 可视化：DNA 双螺旋结构 ---
st.subheader("1. 分子层面：DNA 双螺旋轨道")

# 生成双螺旋的 HTML/CSS 代码
# 我们生成 12 个碱基对作为展示区域
num_pairs = 12
# 计算有多少个位置被甲基化 (从左边开始逐渐增加)
methyl_count = int((methylation_level / 100) * num_pairs)

dna_html = '<div style="display: flex; justify-content: center; align-items: center; height: 200px; overflow-x: auto; padding: 20px; background: #f4f4f9; border-radius: 15px; border: 1px solid #ddd;">'

for i in range(num_pairs):
    # 判断当前位置是否有甲基化
    is_methylated = i < methyl_count
    
    # 颜色设置
    if is_methylated:
        # 甲基化：红色警告色
        color = "#ff4d4d" 
        label = '<div style="position: absolute; top: -35px; color: red; font-weight: bold; font-size: 14px; animation: pop 0.3s;">-CH3</div>'
        glow = "0 0 10px red"
    else:
        # 正常：蓝绿色
        color = "#4facfe"
        label = ""
        glow = "none"

    # 利用正弦波模拟双螺旋的交错感
    # 偶数位置：上链在前，下链在后 (视觉上)
    # 奇数位置：下链在前，上链在后
    
    # 上链节点
    top_node = f'''
    <div style="position: relative; width: 40px; height: 40px; background: {color}; border-radius: 50%; box-shadow: {glow}; z-index: {2 if i%2==0 else 1}; display: flex; justify-content: center; align-items: center; color: white; font-weight: bold; border: 2px solid white;">
        {label}
        A
    </div>
    '''
    
    # 中间连接键 (氢键)
    link_node = f'<div style="width: 10px; height: 4px; background: #ccc;"></div>'
    
    # 下链节点
    bottom_node = f'''
    <div style="position: relative; width: 40px; height: 40px; background: {color}; border-radius: 50%; box-shadow: {glow}; z-index: {2 if i%2!=0 else 1}; display: flex; justify-content: center; align-items: center; color: white; font-weight: bold; border: 2px solid white;">
        T
    </div>
    '''
    
    # 垂直排列这一组
    pair_html = f'<div style="display: flex; flex-direction: column; align-items: center; margin: 0 5px;">{top_node}{link_node}{bottom_node}</div>'
    dna_html += pair_html

dna_html += '</div>'

# 渲染 DNA 结构
st.markdown(dna_html, unsafe_allow_html=True)

# 状态描述
if methylation_level > 70:
    st.error(f"⛔ **转录受阻**：高密度的 -CH3 基团改变了 DNA 结构，RNA 聚合酶无法结合。")
else:
    st.success(f"✅ **转录正常**：DNA 结构开放，允许酶结合。")

# --- 8. 表型展示 ---
st.subheader("2. 宏观表型：小鼠毛色")

col1, col2 = st.columns([1, 2])
with col1:
    try:
        st.image(mouse_img, caption=f"基因状态：{gene_activity}", use_column_width=True)
    except:
        st.error("图片未找到，请检查文件名")
        
with col2:
    st.markdown(f"""
    ### 📊 实验结果分析
    - **当前甲基化水平**: {methylation_level}%
    - **基因表达状态**: {gene_activity}
    - **表型结果**: 小鼠呈现 **{mouse_status.split('(')[0].strip()}** 毛色。
    
    > **原理**：DNA 甲基化通常发生在 CpG 岛。当这些区域被甲基化（加上 -CH3 基团）时，会物理性地阻碍转录因子和 RNA 聚合酶的结合，从而导致基因沉默。
    """)
