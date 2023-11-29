import streamlit as st

def home():
    st.title("Image Steganography App")
    st.image('homepic.png', use_column_width=True)
    st.write(
        "Explore the world of image steganography with this easy-to-use web application. "
        "Encode secret messages within images or decode hidden messages from stego images. "
        "Protect your confidential information and uncover hidden communications. Get started by selecting an operation from the sidebar."
    )

    st.header("What is Image Steganography?")
    st.write(
        "Image steganography is the practice of hiding a piece of information within another image. "
        "In this app, we use steganography to encode text messages or image files within image files. "
        "We will be using the Least-Significant-Bit Algorithm as our methodology."
    )

    st.header("Working of LSB?")
    st.write(
        "The Least Significant Bit (LSB) algorithm is a common technique used in image steganography to embed information within the least significant bits of the pixel values in an image. The algorithm takes advantage of the fact that small changes in the least significant bits are often imperceptible to the human eye, making it a suitable method for hiding data."
    )

    st.image('workinglsb.webp', caption="Pixel Structure", use_column_width=True)

    st.header("How to Use")
    st.write(
        "1. **Encode**: Upload a cover image, enter your secret text, and optionally set a password. "
        "The app will encode the text into the image, and you can download the stego image."
    )

    st.image('encodelsb.png', caption="Encoding Methodology", use_column_width=True)

    st.write(
        "2. **Decode**: Upload a stego image, and if applicable, enter the password used during encoding. "
        "The app will decode the hidden message within the image."
    )

    st.image('decodelsb.png', caption="Decoding Methodology", use_column_width=True)


    st.header("About")
    st.write(
        "This app is created using Streamlit, a simple and powerful framework for creating web applications with Python."
        "It leverages image processing libraries such as OpenCV and Pillow."
    )
    st.write("Made with ❤️ by Melbin and Aaron")

    st.header("References")
    st.markdown(
        "- [https://docs.streamlit.io/](https://docs.streamlit.io/)"
    )
    st.markdown(
        "- [https://www.javatpoint.com/image-steganography-using-python](https://www.javatpoint.com/image-steganography-using-python)"
    )
    st.markdown(
        "- [https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2](https://medium.com/swlh/lsb-image-steganography-using-python-2bbbee2c69a2)"
    )
    st.markdown(
        "- [https://medium.com/analytics-vidhya/shh-your-secret-is-safe-a-simple-guide-to-steganography-in-python-89116582277e](https://medium.com/analytics-vidhya/shh-your-secret-is-safe-a-simple-guide-to-steganography-in-python-89116582277e)"
    )

if __name__ == "__main__":
    home()
