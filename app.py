import streamlit as st
from PIL import Image
import subprocess
import os


st.session_state['send_clicked'] = False
image_path = './placeholder.jpg'
default_image = Image.open(image_path)

st.set_page_config(layout="wide", page_title="LlaVA")

st.write("## LLaVA-GUI: Large Language and Vision Assistant")
st.write(
    ""
)
col1, col2 = st.columns(2)
st.sidebar.write("## Upload an image:")


uploaded_image = st.sidebar.file_uploader("uploader", type=["jpg", "jpeg"], label_visibility='hidden')
inference_result_box = st.sidebar.empty()

if uploaded_image:
    col1.image(uploaded_image)
    image_path = os.path.join("./", uploaded_image.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
else:
    col1.image(default_image)

user_question = col1.text_input(label='user_query', placeholder="Ask your question about the image",
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

send_btn = col1.button("Send")

if send_btn:
    if not uploaded_image:
        st.warning('Please upload an image first', icon="⚠️")
    else:
        st.session_state['send_clicked'] = True
        query = user_question or "describe the image in detail."
        command = ["./llava", "-m", "models/ggml-model-q4_k.gguf", "--mmproj", "models/mmproj-model-f16.gguf", "--temp",
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
        st.success('Done!')

st.markdown('#')
with st.expander("Terms of use"):
    st.write(
        "By using this service, users are required to agree to the following terms: The service is a research preview intended for non-commercial use only. It only provides limited safety measures and may generate offensive content. It must not be used for any illegal, harmful, violent, racist, or sexual purposes. The service may collect user dialogue data for future research. Please click the “Flag” button if you get any inappropriate answer! We will collect those to keep improving our moderator. For an optimal experience, please use desktop computers for this demo, as mobile devices may compromise its quality.")
