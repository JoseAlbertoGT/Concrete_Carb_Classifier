# This script runs in the TensorFlow environment --- ROG ZEPHYRUS
# This script runs in the Streamlit environment --- ROG STRIX

# Libraries
import tensorflow as tf
import streamlit as st
import numpy as np
import os
import platform
from Utilities import set_page_configuration
from streamlit_lottie import st_lottie
from Utilities import load_lottiefile
from Utilities import background

# -------------------- Cleaning the terminal -------------------- #
os.system('cls')

# -------------------- Defining main functions -------------------- #
def verify_environment():
    system = platform.system()
    if system == "Windows":
        device = tf.test.gpu_device_name()
        if device:
            st.sidebar.success("Running on GPU: " + device)
        else:
            st.sidebar.warning("Running on CPU only")
    return True

def authenticate_user():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        with st.sidebar:
            password = st.text_input("Enter access code:", type="password")
            if password == "concrete2024":  # Simple example password
                st.session_state.authenticated = True
            elif password:
                st.error("Invalid access code")
    return st.session_state.authenticated

def load_image_tf(filename):
    try:
        # loading the image
        img = tf.keras.utils.load_img(filename, target_size=(224, 224))
        # Input validation
        if img.size == 0:
            st.error("Invalid image file")
            return None
        # Converting to an array
        img = tf.keras.utils.img_to_array(img)
        # Reshaping into a single sample with 3 channels
        img = img.reshape(1,224, 224, 3)
        # Center pixel data
        img = img.astype("float32")
        img = img - [123.68, 116.779, 103.939]
        return img
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

def run_classifier(img):
    try:
        if img is None:
            return None
        # Loading the model
        model = tf.keras.models.load_model("carbonation_classifier_model.h5")
        # Predicting the class
        result = model.predict(img)
        final_response = result[0][0]
        print(final_response)
        if final_response <= 0.22: # Here we define the Certainty of the model
            st.write(":green[The concrete sample image has carbonation-free zones 🤖]")
            st.write(f":green[The model's accuracy of this model for this image is:] :blue[{99.07}%]")
        else:
            st.write(":orange[The concrete sample image has damage of carbonation 🤖]")
            st.write(f":orange[The model's accuracy of this model for this image is:] :blue[{99.07}%]")

        return result
    except Exception as e:
        st.error(f"Error during classification: {str(e)}")
        return None
	
# -------------------- Setting the main page of the webapp -------------------- #
set_page_configuration()
background("Images/side_bar_img.png")

# Hidding the hamburger button
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Hidding the Github button
hide_github_icon = """
<style>
#GithubIcon {visibility: hidden;}
footer {visibility: hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

st.title(":green[Concrete Carbonation Classifier]🧑‍🔬" )
st.divider()

lottie_animation = load_lottiefile("Gifs/Animation.json")
st_lottie(lottie_animation, height=200, quality="high")

# -------------------- Setting the sidebar of the webapp -------------------- #
with st.sidebar.container():
	# st.image("Images/logo_siiia_b.png")
	st.image(image="Images/icon.webp")
	st.logo(image="Images/icon.webp", size="large")

with st.sidebar.expander(label=":orange[About]"):
	st.html("""<h5 style = 'text-align:justify'>
		Concrete Carbonation Classifier <br>
		Version: 1.0.3 <br>
		Date: Feb-28-2024
		</h5>
""")

# Contatc information
with st.sidebar.expander(label=":orange[About the Author]"):
	st.html("""<h5 style = 'text-align:center; color:black'>
		Dr. José Alberto Guzmán Torres
		Posdoctoral Researcher
		UMSNH-México
		Civil Engineering Faculty <br>
		Personal Profiles: </h5>""")
	st.markdown("🧑‍🔬 [:green[ResearcGate]](https://www.researchgate.net/profile/Jose-Guzman-Torres)")
	st.markdown("📚 [:green[Scholar Google]](https://scholar.google.com.mx/citations?user=lZA3PrIAAAAJ&hl=es&authuser=1)")
	st.markdown("👷 [:green[Linkedin]](https://www.linkedin.com/in/jos%C3%A9-alberto-guzm%C3%A1n-torres-b4224372/)")

with st.sidebar.expander(label=":orange[Sponsors]"):
	st.markdown("[SECIHTI](https://conahcyt.mx/)")
	st.markdown("[UMSNH](https://www.umich.mx/)")
	st.markdown("[Sistema SNII](https://conahcyt.mx/servicios-en-linea/sistema-snii/)")
	st.markdown("[SIIIA MATH](https://siiia.org/)")

with st.sidebar.container():
	st.image("Images/logo_siiia_b.png")

# -------------------- Setting the interface of the webapp -------------------- #
if authenticate_user():
    with st.container(border=True):
        st.subheader("Description", divider=True)
        st.html("""<h6 style = 'text-align:justify'> Concrete Carbonation Classifier is an advanced web app designed for engineers and researchers in civil engineering,
        specializing in the automated classification of concrete samples based on carbonation damage. 
        Powered by artificial intelligence, this tool employs a convolutional neural network (CNN) model
        trained to recognize patterns in concrete samples and determine their level of carbonation. 
        By simply uploading an image of a concrete sample, users can quickly receive accurate assessments 
        of carbonation presence, aiding in the early detection of structural vulnerabilities and supporting 
        maintenance decisions. This tool offers an efficient, AI-driven approach to monitoring concrete integrity,
        helping extend the lifespan of infrastructure through precise diagnostics. </h6>
            """)

    with st.expander(label="Classify an image:"):
        image = st.file_uploader(label="📂 Upload a concrete sample image:")
        st.write(":orange[Warning: In order to avoid mistakes, make sure that your image is about a concrete sample!!]")
        col1, col2, col3, = st.columns(3, vertical_alignment="center")
        with col2:
            if image is not None:
                st.image(image=image, caption="Uploaded image", use_container_width=True)

        with st.form(key="Image_classifier"):
            submit_button = st.form_submit_button(label="Classify", type="primary")
                
            if submit_button:
                if image is None:
                    st.write(":red[Please, upload an image or select a testing image!!] 😅")
                else:
                    img = load_image_tf(filename=image)
                    st.html("<h3 style='color:green'> Results: </h3>")
                    result_model = run_classifier(img=img)
        
        # Mapping for testing images: display name -> file path
        testing_images = {
            "Sample Image 1": "Images/Sample images/Sample_.jpg",
            "Sample Image 2": "Images/Sample images/Sample_image (1).jpg",
            "Sample Image 3": "Images/Sample images/Sample_image (2).jpg",
            "Sample Image 4": "Images/Sample images/Sample_image (3).jpg"
        }
        
        with st.container(key="testing_images", border=True):
            option = st.selectbox(
                placeholder="Choose an option",
                label="📂 Select testing image:", index=None,
                options=list(testing_images.keys())
            )
            
            if option:
                selected_image_path = testing_images[option]
                col1, col2, col3, = st.columns(3, vertical_alignment="center")
                with col2:
                    st.image(image=selected_image_path, caption="Testing image", use_container_width=True)
                    
                    img_test = load_image_tf(filename=selected_image_path)
                
                    st.html("<h3 style='color:green'> Results: </h3>")
                    result_model_test = run_classifier(img=img_test)
else:
    st.warning("Please enter access code to use the classifier")

# -------------------- Space for dubugging in terminal -------------------- #

st.html("<h5 style='text-align:center'> © Concrete Carbonation classifier. All rights reserved. </h5>")

with st.container(height=200, border=False):
	col1, col2, col3 = st.columns(3,vertical_alignment="center", gap="small")
	with col2:
		col1, col2, col3= st.columns(3, vertical_alignment="center", gap="small")
		with col1:
			st.image(image="Images/logotipo_SCyT.svg", width=400, use_container_width=True)
		with col2:		
			st.image(image="Images/logo_siiia_w.png", width=400, use_container_width=True)
		with col3:
			st.image(image="Images/UMSNH.png", width=90, use_container_width=True)