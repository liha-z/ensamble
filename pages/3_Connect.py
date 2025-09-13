import streamlit as st
import base64

# Sets up the Streamlit UI elements and show contact info.

st.set_page_config(page_title="ensamble.ai", page_icon=":tada:", layout="wide")
st.sidebar.header("Contact Us")

def img_to_bytes(img_path):
    img_bytes = None
    try:
        with open(img_path, "rb") as img_file:
            img_bytes = img_file.read()
    except FileNotFoundError:
        print(f"Error: Image file not found at {img_path}")
    return img_bytes

img_bytes = img_to_bytes("mypic.png")

if img_bytes:
    img_str = base64.b64encode(img_bytes).decode()
    img_html = f'<img src="data:image/png;base64,{img_str}" style="width:200px;height:200px;border-radius:50%;display:inline-block;vertical-align:middle;">'
    st.markdown(img_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)  # to get blank lines
    st.write("Sahil Ali Akhtar")
    st.write("I learned from my observations that we tend to lose things we don't care about. That's why I am passionate about creating a better world using whatever we have at hand. If you have an interesting idea, please feel free to write. I also enjoy eccentric discussions about life, dogs and coffee;)")
    st.write("Write me at : rsahil0211@gmail.com")
else:
    st.write("Image not found. Please check the file path.")