import streamlit as st
from cv2 import imread, imwrite
from base64 import urlsafe_b64encode
from hashlib import md5
from cryptography.fernet import Fernet
from PIL import Image
import os

class FileError(Exception):
    pass

class DataError(Exception):
    pass

class PasswordError(Exception):
    pass


def save_image(uploaded_file):
    save_folder = "saved_images"
    os.makedirs(save_folder, exist_ok=True)

    image_name = uploaded_file.name
    save_path = os.path.join(save_folder, image_name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    return save_path

def encrypt_decrypt(string, password, mode='enc'):
    _hash = md5(password.encode()).hexdigest()
    cipher_key = urlsafe_b64encode(_hash.encode())
    cipher = Fernet(cipher_key)
    if mode == 'enc':
        return cipher.encrypt(string.encode()).decode()
    else:
        return cipher.decrypt(string.encode()).decode()

def str2bin(string):
    return ''.join((bin(ord(i))[2:]).zfill(8) for i in string)

def bin2str(string):
    return ''.join(chr(int(string[i:i+8], 2)) for i in range(0, len(string), 8))

def encode(input_filepath, text, output_filepath, password=None):
    if password is not None:
        data = encrypt_decrypt(text, password, 'enc')
    else:
        data = text

    data_length = bin(len(data))[2:].zfill(32)
    bin_data = iter(data_length + str2bin(data))
    img = imread(input_filepath, 1)

    if img is None:
        raise FileError(f"The image file '{input_filepath}' is inaccessible")

    height, width = img.shape[0], img.shape[1]
    encoding_capacity = height * width * 3
    total_bits = 32 + len(data) * 8

    if total_bits > encoding_capacity:
        raise DataError("The data size is too big to fit in this image!")

    completed = False
    modified_bits = 0

    for i in range(height):
        for j in range(width):
            pixel = img[i, j]

            for k in range(3):
                try:
                    x = next(bin_data)
                except StopIteration:
                    completed = True
                    break

                if x == '0' and pixel[k] % 2 == 1:
                    pixel[k] -= 1
                    modified_bits += 1
                elif x == '1' and pixel[k] % 2 == 0:
                    pixel[k] += 1
                    modified_bits += 1

            if completed:
                break

        if completed:
            break

    written = imwrite(output_filepath, img)

    if not written:
        raise FileError(f"Failed to write image '{output_filepath}'")

    loss_percentage = (modified_bits / encoding_capacity) * 100
    return loss_percentage

def decode(input_filepath, password=None):
    result, extracted_bits, completed, number_of_bits = '', 0, False, None
    img = imread(input_filepath)

    if img is None:
        raise FileError(f"The image file '{input_filepath}' is inaccessible")

    height, width = img.shape[0], img.shape[1]

    for i in range(height):
        for j in range(width):
            for k in img[i, j]:
                result += str(k % 2)
                extracted_bits += 1

                if extracted_bits == 32 and number_of_bits is None:
                    number_of_bits = int(result, 2) * 8
                    result = ''
                    extracted_bits = 0
                elif extracted_bits == number_of_bits:
                    completed = True
                    break

            if completed:
                break

        if completed:
            break

    if password is None:
        return bin2str(result)
    else:
        try:
            return encrypt_decrypt(bin2str(result), password, 'dec')
        except:
            raise PasswordError("Invalid password!")

# Streamlit Application
st.title("Text-in-Image Steganography")

choice = st.radio("Select an operation:", ("Encode", "Decode"))

if choice == "Encode":
    st.header("Encode Image")

    st.info("Upload a cover image to encode a message.")

    ip_file = st.file_uploader("Upload Cover Image", type=["png"])
    if ip_file is not None:
        image = Image.open(ip_file)
        st.image(image, caption="Uploaded Image", width=300)
    text = st.text_area("Enter Secret Data") #Give height
    pwd = st.text_input("Enter Password (optional)")

    if st.button("Encode"):
        if ip_file is not None and text != "":
            try:
                with st.spinner("Encoding..."):
                    save_path = save_image(ip_file)
                    output_path = os.path.join("saved_images", "encoded_image.png")
                    loss = encode(save_path, text, output_path, pwd)
                    encoded_image = Image.open(output_path)
                    
                    st.success(f"Successfully Encoded! Download Image below.")
                    download_button = st.download_button(
                    label="Download Encoded Image",
                    data=open(output_path, "rb").read(),
                    key="download_button",
                    file_name="encoded_image.png",
                    mime="image/png",
                    )

            except FileError as fe:
                st.error(f"Error: {fe}")
            except DataError as de:
                st.error(f"Error: {de}")
        else:
            st.warning("Please upload an image and enter text.")

elif choice == "Decode":
    st.header("Decode Image")

    st.info("Upload a stego image to decode the hidden message.")

    stego_image = st.file_uploader("Upload Stego Image", type=["png"])
    if stego_image is not None:
        image = Image.open(stego_image)
        st.image(image, caption="Uploaded Image", width=300)
    pwd_decode = st.text_input("Enter Password (if applicable)")


    if st.button("Decode"):
        if stego_image is not None:
            try:
                with st.spinner("Decoding..."):
                    save_path = save_image(stego_image)
                    decoded_text = decode(save_path, pwd_decode)
                    st.success(f"Decoded Message: {decoded_text}")
            except FileError as fe:
                st.error(f"Error: {fe}")
            except PasswordError as pe:
                st.error(f"Error: {pe}")
        else:
            st.warning("Please upload a stego image.")