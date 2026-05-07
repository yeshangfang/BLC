import streamlit as st
from PIL import Image
import numpy as np

# 定义DNA轨道的长度
dna_length = 20

# 创建一个函数来绘制DNA轨道和甲基化状态
def draw_dna(methylation_level):
    dna_track = ['A-T' if i % 2 == 0 else 'C-G' for i in range(dna_length)]
    methylation_sites = [i for i in range(dna_length) if np.random.rand() < methylation_level / 100.0]
    
    # 绘制DNA轨道
    dna_str = ''
    for i, base_pair in enumerate(dna_track):
        if i in methylation_sites:
            dna_str += f'{base_pair}-CH3 '
        else:
            dna_str += f'{base_pair}     '
    
    return dna_str.strip()

# 创建一个函数来获取小鼠毛色图像
def get_mouse_color_image(gene_expression):
    if gene_expression > 50:
        return Image.open('white_mouse.png')  # 假设白色代表基因表达正常
    elif gene_expression < 30:
        return Image.open('black_mouse.png')  # 假设黑色代表基因被抑制
    else:
        return Image.open('gray_mouse.png')   # 假设灰色代表中间状态

# 设置页面标题
st.title("DNA甲基化模拟器")

# 添加滑块以控制甲基化水平
methylation_level = st.slider("DNA甲基化水平 (%)", min_value=0, max_value=100, value=50)

# 计算基因表达水平（简化模型）
gene_expression = 100 - methylation_level

# 显示DNA轨道和甲基化状态
dna_str = draw_dna(methylation_level)
st.text(f"DNA 轨道: {dna_str}")

# 显示基因表达水平
st.write(f"基因表达水平: {gene_expression}%")

# 显示小鼠毛色图像
mouse_color_image = get_mouse_color_image(gene_expression)
st.image(mouse_color_image, caption="小鼠毛色变化", width=200)
