import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw

# Function to draw DNA double helix
def draw_dna(ax, methylation_level):
    # Parameters for DNA structure
    num_turns = 10
    radius = 2
    pitch = 3.4
    
    # Create a spiral path for DNA
    theta = np.linspace(0, 2 * np.pi * num_turns, 100)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    z = (theta / (2 * np.pi)) * pitch
    
    # Plot two strands of DNA
    ax.plot(x, y, z, color='blue', label='Strand 1')
    ax.plot(-x, -y, z, color='green', label='Strand 2')
    
    # Highlight methylated regions on one strand
    if methylation_level > 0:
        start_index = int((1 - methylation_level) * len(theta))
        end_index = len(theta)
        ax.plot(x[start_index:end_index], y[start_index:end_index], z[start_index:end_index], color='red', linewidth=5)

# Function to create cartoon mouse with fur color based on methylation level
def create_mouse(methylation_level):
    base_color = (255, 255, 255)  # White base color
    dark_color = (192, 192, 192)   # Dark gray for methylated effect
    
    # Mix colors based on methylation level
    mixed_color = tuple(int(base + (dark - base) * methylation_level) for base, dark in zip(base_color, dark_color))
    
    # Create an image of a simple cartoon mouse
    img = Image.new('RGB', (100, 100), color=mixed_color)
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 80, 80], fill=mixed_color)  # Body
    draw.rectangle([40, 60, 60, 70], fill=(0, 0, 0))   # Tail
    draw.ellipse([30, 30, 40, 40], fill=(0, 0, 0))     # Left ear
    draw.ellipse([60, 30, 70, 40], fill=(0, 0, 0))     # Right ear
    draw.ellipse([40, 40, 50, 50], fill=(0, 0, 0))     # Eye
    draw.line([40, 40, 50, 50], fill=(0, 0, 0), width=2)  # Nose
    
    return img

# Streamlit app
st.title("DNA Methylation Simulation")

# Slider for methylation level
methylation_level = st.slider("Methylation Level", min_value=0.0, max_value=1.0, value=0.0, step=0.01)

# Display DNA double helix
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
draw_dna(ax, methylation_level)
ax.set_axis_off()
st.pyplot(fig)

# Display cartoon mouse
mouse_image = create_mouse(methylation_level)
st.image(mouse_image, caption="Cartoon Mouse Phenotype")
