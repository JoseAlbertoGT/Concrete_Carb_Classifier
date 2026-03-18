
import streamlit as st
import base64
import json

# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Team Research - Concrete Carbonation Classifier",
    page_icon="Images/icon.webp",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Background of the Sidebar (copied from Utilities.py)
class background:
    def __init__(self, img):
        self.img = img
        side_bg_ext = "webp"
        side_bg = self.img

        st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
        background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
        }}
        </style>
        """,
        unsafe_allow_html = True,
        )

# Setting animations (copied from Utilities.py)
def load_lottiefile(filename: str):
                with open(file=filename, mode='r') as f:
                    return json.load(f)

# Set background for the sidebar
try:
    background("Images/side_bar_img.png")
except:
    pass

# Hidding the hamburger button (copied from Central_app.py)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Hidding the Github button (copied from Central_app.py)
hide_github_icon = """
<style>
#GithubIcon {visibility: hidden;}
footer {visibility: hidden;}
header {visibility:hidden;}
</style>
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

# Sidebar Content (copied from Central_app.py)
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
    st.markdown("---")
    st.markdown("🏠 [:orange[Volver al inicio]](/Central_app)")

with st.sidebar.expander(label=":orange[Sponsors]"):
    st.markdown("[:green[SECIHTI]](https://conahcyt.mx/)")
    st.markdown("[:green[UMSNH]](https://www.umich.mx/)")
    st.markdown("[:green[Sistema SNII]](https://conahcyt.mx/servicios-en-linea/sistema-snii/)")
    st.markdown("[:green[SIIIA MATH]](https://siiia.com.mx/)")

with st.sidebar.container():
    st.image("Images/logo_siiia_b.png")

# Title
st.title("🔬 Team Research")
st.markdown("---")

# Principal Researchers Section
st.subheader("👨‍🔬 Principal Researchers")

# Creating columns for the researchers
# First Row
col1, col2, col3 = st.columns(3)

with col1:
    st.image("Public/docs/Images/JAGT1.jpg", use_container_width=True)
    st.markdown("""
    **Dr. José Alberto Guzmán Torres** 🇲🇽
    
    *   🏢 [SIIIA MATH: Soluciones en ingeniería](http://www.siiia.com.mx)
    *   🏛️ [Universidad Michoacana de San Nicolás de Hidalgo](http://www.umich.mx)
    *   🔬 Engineering applications & Artificial Intelligence
    *   📧 jose.alberto.guzman@umich.mx
    *   🌐 [ORCID](https://orcid.org/0000-0002-9309-9390)
    """)

with col2:
    st.image("Public/docs/Images/FJDM1.jpg", use_container_width=True)
    st.markdown("""
    **Dr. Francisco Javier Domínguez Mota** 🇲🇽
    
    *   🏢 [SIIIA MATH: Soluciones en ingeniería](http://www.siiia.com.mx)
    *   🏛️ [Universidad Michoacana de San Nicolás de Hidalgo](http://www.umich.mx)
    *   🔬 Applied Mathematics & Finite Difference Methods
    *   📧 francisco.mota@umich.mx
    *   🌐 [ORCID](https://orcid.org/0000-0001-6837-172X)
    """)

with col3:
    st.image("Public/docs/Images/GTG.jpg", use_container_width=True)
    st.markdown("""
    **Dr. Gerardo Tinoco Guerrero** 🇲🇽
    
    *   🏢 [SIIIA MATH: Soluciones en ingeniería](http://www.siiia.com.mx)
    *   🏛️ [Universidad Michoacana de San Nicolás de Hidalgo](http://www.umich.mx)
    *   🔬 Numerical Methods & Computational Mathematics
    *   📧 gerardo.tinoco@umich.mx
    *   🌐 [ORCID](https://orcid.org/0000-0003-3119-770X)
    """)

st.markdown("---")

# Second Row
col4, col5, col6 = st.columns(3)

with col4:
    st.image("Public/docs/Images/JGTR1.jpg", use_container_width=True)
    st.markdown("""
    **Dr. José Gerardo Tinoco Ruíz** 🇲🇽
    
    *   🏢 [SIIIA MATH: Soluciones en ingeniería](http://www.siiia.com.mx)
    *   🏛️ [Universidad Michoacana de San Nicolás de Hidalgo](http://www.umich.mx)
    *   🔬 Applied Mathematics & Scientific Computing
    *   📧 jose.gerardo.tinoco@umich.mx
    *   🌐 [ORCID](https://orcid.org/0000-0002-0866-4798)
    """)

with col5:
    st.image("Public/docs/Images/EMAG.jpg", use_container_width=True)
    st.markdown("""
    **Dra. Elia Mercedes Alonso Guzmán** 🇲🇽
    
    *   🏢 [SIIIA MATH: Soluciones en ingeniería](http://www.siiia.com.mx)
    *   🏛️ [Universidad Michoacana de San Nicolás de Hidalgo](http://www.umich.mx)
    *   🔬 Civil Engineering & Materials Science
    *   📧 elia.alonso@umich.mx
    *   🌐 [ORCID](https://orcid.org/0000-0002-8502-4313)
    """)

with col6:
    st.image("Public/docs/Images/Harias.webp", use_container_width=True)
    st.markdown("""
    **Dr. Heriberto Arias Rojas** 🇲🇽
    
    *   🏢 [SIIIA MATH: Soluciones en ingeniería](http://www.siiia.com.mx)
    *   🏛️ [Universidad Michoacana de San Nicolás de Hidalgo](http://www.umich.mx)
    *   🔬 Computer Science & Data Analysis
    *   📧 heriberto.arias@umich.mx
    *   🌐 [ORCID](https://orcid.org/0000-0002-7641-8310)
    """)

st.markdown("---")
st.markdown("<h5 style='text-align:center'> © Concrete Carbonation classifier. All rights reserved. </h5>", unsafe_allow_html=True)
