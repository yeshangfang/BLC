import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np

# Function to draw DNA double helix
def draw_dna(ax, methylation_level):
    # Parameters for the DNA structure
    num_turns = 3
    radius = 0.5
    pitch = 2 * np.pi / num_turns
    
    # Generate points for one turn of the helix
    t = np.linspace(0, num_turns * 2 * np.pi, 1000)
    x = radius * np.cos(t)
    y = radius * np.sin(t)
    z = t * pitch / (num_turns * 2 * np.pi)
    
    # Plot two strands of DNA
    ax.plot(x, y, z, color='blue', lw=2)
    ax.plot(-x, -y, z, color='green', lw=2)
    
    # Add methyl groups based on methylation level
    for i in range(int(methylation_level * len(t))):
        if i % 10 == 0:  # Only add every 10th point for visualization purposes
            angle = t[i]
            mx = radius * 1.1 * np.cos(angle)
            my = radius * 1.1 * np.sin(angle)
            mz = z[i]
            ax.scatter(mx, my, mz, color='red', s=10)  # Red dot representing a methyl group

# Function to display mouse phenotype image
def get_mouse_phenotype_image(methylation_level):
    base_image_path = "mouse_base.png"
    white_image_path = "mouse_white.png"
    black_image_path = "mouse_black.png"
    
    base_img = Image.open(base_image_path).convert("RGBA")
    white_img = Image.open(white_image_path).convert("RGBA")
    black_img = Image.open(black_image_path).convert("RGBA")
    
    mask = Image.new('L', base_img.size, int(methylation_level * 255))
    composite_img = Image.composite(white_img, black_img, mask)
    final_img = Image.alpha_composite(base_img, composite_img)
    
    return final_img

# Main function to run the Streamlit app
def main():
    st.title("DNA Methylation and Gene Transcription Simulation")
    
    methylation_level = st.slider("Methylation Level", min_value=0.0, max_value=1.0, step=0.01)
    
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(projection='3d')
    draw_dna(ax, methylation_level)
    ax.set_axis_off()
    st.pyplot(fig)
    
    mouse_image = get_mouse_phenotype_image(methylation_level)
    st.image(mouse_image, caption="Mouse Phenotype")

if __name__ == "__main__":
    main()
