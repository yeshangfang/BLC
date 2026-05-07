import streamlit as st

# --- 1. 页面基础设置 ---
st.set_page_config(page_title="DNA甲基化模拟器", layout="centered")

# --- 2. 定义图片路径 ---
# 这里对应你上传的三个文件名，注意后缀名要一致（比如都是 .png 或 .jpg）
# 如果你上传的文件名是 black mouse.png (带空格)，请在这里改成 "black mouse.png"
IMG_BLACK = "black.png"
IMG_WHITE = "white.png"
IMG_GREEN = "green.png"

# --- 3. 侧边栏说明 ---
st.sidebar.header("🧬 实验控制台")
st.sidebar.write("拖动滑块，模拟甲基化基团(-CH3)的数量变化。")
st.sidebar.write("- **0% 甲基化**：基因开启（绿色小鼠）")
st.sidebar.write("- **50% 甲基化**：基因减弱（黑色小鼠）")
st.sidebar.write("- **100% 甲基化**：基因关闭（白色小鼠）")

# --- 4. 主界面标题 ---
st.title("DNA 甲基化：基因表达的“红绿灯”")
st.markdown("---")

# --- 5. 核心交互：滑块 ---
# 滑块范围 0 到 100，代表甲基化程度
methylation_level = st.slider(
    "🧪 调节 DNA 甲基化程度",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)

# --- 6. 逻辑判断：根据滑块数值决定显示哪只小鼠 ---
# 我们将甲基化程度分为三段
if methylation_level < 30:
    selected_mouse = IMG_GREEN  # 低甲基化 -> 绿色（基因活跃）
    status_text = "🟢 基因表达活跃"
    polymerase_status = "✅ RNA聚合酶顺利结合"
elif 30 <= methylation_level < 70:
    selected_mouse = IMG_BLACK  # 中甲基化 -> 黑色（基因受抑）
    status_text = "⚫ 基因表达受抑"
    polymerase_status = "⚠️ RNA聚合酶结合受阻"
else:
    selected_mouse = IMG_WHITE  # 高甲基化 -> 白色（基因沉默）
    status_text = "⚪ 基因完全关闭 (沉默)"
    polymerase_status = "❌ RNA聚合酶无法结合"

# --- 7. 可视化展示区域 ---

# 第一行：DNA 轨道与聚合酶状态
st.subheader("1. 分子层面：DNA 轨道")

# 模拟 DNA 轨道上的 -CH3 (甲基)
# 我们生成 10 个位置，根据甲基化程度决定显示多少个 -CH3
dna_track = ""
num_methyl_groups = int(methylation_level / 10) # 0到10个甲基

for i in range(10):
    if i < num_methyl_groups:
        # 红灯/甲基化：用红色方块或文字表示阻碍
        dna_track += f"🛑<sub>CH3</sub> " 
    else:
        # 绿灯/无甲基化：用绿色竖线表示DNA骨架
        dna_track += f"🟢<sub>|</sub> "

# 显示 DNA 轨道 (使用 HTML 渲染下标)
st.markdown(f"""
    <div style="background-color:#f0f2f6; padding:20px; border-radius:10px; border: 1px solid #ccc;">
        <p style="font-family: 'Courier New', monospace; font-size: 18px; line-height: 1.5;">
            5' - {dna_track} - 3'
        </p >
    </div>
    """, unsafe_allow_html=True)

st.info(f"**当前状态：** {status_text} \n\n **聚合酶情况：** {polymerase_status}")

# 第二行：表型展示
st.subheader("2. 宏观表型：小鼠毛色")

# 显示对应的小鼠图片
# 使用 use_column_width=True 让图片自适应屏幕宽度
try:
    st.image(selected_mouse, caption=f"表型结果: {status_text}", use_column_width=True)
except Exception as e:
    st.error("❌ 图片未找到！请检查 GitHub 仓库中是否上传了以下文件：")
    st.write(f"- {IMG_BLACK}")
    st.write(f"- {IMG_WHITE}")
    st.write(f"- {IMG_GREEN}")
    st.write("⚠️ 注意：文件名区分大小写，且后缀名（.png 或 .jpg）必须一致。")
