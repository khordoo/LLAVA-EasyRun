import streamlit as st
from PIL import Image
import subprocess
import os

GGML_MODEL_Path = 'models/ggml-model-q4_k.gguf'
MMPROJ_PATH = "models/mmproj-model-f16.gguf"

image_path = './placeholder.jpg'
default_image = Image.open(image_path)

st.set_page_config(layout="wide", page_title="LlaVA")

st.write("## LLaVA-GUI: Large Language and Vision Assistant")
left_col, _ = st.columns(2)
st.sidebar.write("## Upload an image:")

uploaded_image = st.sidebar.file_uploader("uploader", type=["jpg", "jpeg"], label_visibility='hidden')
inference_result_box = st.sidebar.empty()

if uploaded_image:
    left_col.image(uploaded_image)
    image_path = os.path.join("./", uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
else:
    left_col.image(default_image)

user_question = left_col.text_input(label='user_query', placeholder="Ask your question about the image",
                                    label_visibility='hidden')

st.markdown("""
   <style>
   div.stButton > button:first-child {
       background-color: #FF8C00;
       color:#ffffff;
   }
   div.stButton > button:hover {
       background-color: #FFA500;
       color:#ffffff;
       }
   </style>""", unsafe_allow_html=True)

send_btn = left_col.button("Send")
loading_placeholder = st.empty()


def run_llava(user_question, image_path):
    """
    Runs LLaVA using llama.cpp
    """
    command = ["./llava", "-m", GGML_MODEL_Path, "--mmproj", MMPROJ_PATH, "--temp",
               "0.1", "--image", image_path, "-p", user_question]
    lines = []
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as process:
        while True:
            line = process.stdout.readline()
            if 'llama_print_timings' in line:
                st.sidebar.write(lines[-1])
                process.communicate()
                break
            lines.append(line)
            if not line:
                process.communicate()
                break  # No more data is being generated
    process.wait()


if send_btn:
    with loading_placeholder:
        with st.spinner("Generating..."):
            if not uploaded_image:
                st.warning('Please upload an image first', icon="⚠️")
            else:
                run_llava(user_question, image_path)
        st.success('Done!')

st.markdown('#')
with st.expander("Terms of use"):
    st.write(
        """By using this service, users are required to agree to the following terms:
        The service is a research preview intended for non-commercial use only.
        It only provides limited safety measures and may generate offensive content.
        It must not be used for any illegal, harmful, violent, racist, or sexual purposes.
        For an optimal experience, please use desktop computers for this demo, as mobile devices may compromise its quality.
        """)
