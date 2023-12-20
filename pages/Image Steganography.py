import streamlit as st
from PIL import Image
import io

# Define your functions here

def int2bin(rgb):
    r, g, b = rgb
    return ('{0:08b}'.format(r), '{0:08b}'.format(g), '{0:08b}'.format(b))

def bin2int(rgb):
    r, g, b = rgb
    return (int(r, 2), int(g, 2), int(b, 2))

def merge2rgb2(rgb1, rgb2):
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rgb = (r1[:6] + r2[:2], g1[:6] + g2[:2], b1[:6] + b2[:2])
    return rgb

def merge2img2(img1, img2):
    # Resize image1 to match the size of image2
    img1 = img1.resize(img2.size)

    pixel_map1 = img1.load()
    pixel_map2 = img2.load()

    new_image = Image.new(img2.mode, img2.size)
    pixels_new = new_image.load()

    for i in range(img2.size[0]):
        for j in range(img2.size[1]):
            rgb1 = int2bin(pixel_map1[i, j])
            rgb2 = int2bin(pixel_map2[i, j])

            merge_rgb = merge2rgb2(rgb1, rgb2)
            pixels_new[i, j] = bin2int(merge_rgb)

    return new_image

def unmerge2(img):
    pixel_map = img.load()

    new_image = Image.new(img.mode, img.size)
    pixels_new = new_image.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            r, g, b = int2bin(pixel_map[i, j])

            rgb = (r[6:] + "000000", g[6:] + "000000", b[6:] + "000000")
            pixels_new[i, j] = bin2int(rgb)

# Streamlit app starts here
st.title("Image Steganography App")

# Upload image widgets
uploaded_file1 = st.file_uploader("Upload the carrier image:", type=["jpg", "jpeg", "png"])
uploaded_file2 = st.file_uploader("Upload the secret image to hide:", type=["jpg", "jpeg", "png"])

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Open images
    image1 = Image.open(uploaded_file1)
    image2 = Image.open(uploaded_file2)

    # Display uploaded images
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, caption='Carrier Image', use_column_width=True)
    with col2:
        st.image(image2, caption='Secret Image', use_column_width=True)

    # Steganography
    if st.button('Merge Images'):
        merged_image = merge2img2(image1, image2)
        st.image(merged_image, caption='Merged Image', use_column_width=True)

    # Decrypt Image
    if st.button('Decrypt Image') and 'merged_image' in locals():
        decrypted_image = unmerge2(merged_image)
        st.image(decrypted_image, caption='Decrypted Image', use_column_width=True)

        # Display the original secret image below the decrypted image
        st.image(image2, caption='Original Secret Image', use_column_width=True)
