# Libraries
import streamlit as st
import base64
import json

#----------------------------------------------------------------#
# Background of the Sidebar
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
#----------------------------------------------------------------#
# Setting of the page
class set_page_configuration:
    def __init__(self):
        st.set_page_config(page_title="Concrete Carbonation Classifier",
                        page_icon = "Images/icon.webp",
                        layout="wide",
                        initial_sidebar_state="expanded",
                        menu_items={
        'Get Help': 'https://www.linkedin.com/in/jos%C3%A9-alberto-guzm%C3%A1n-torres-b4224372/',
        'Report a bug': "https://www.linkedin.com/in/jos%C3%A9-alberto-guzm%C3%A1n-torres-b4224372/",
        'About': """### Image Carbonation Classifier.
                    ## This is an *extremely* cool app!"""})
#----------------------------------------------------------------#
# Setting animations
def load_lottiefile(filename: str):
                with open(file=filename, mode='r') as f:
                    return json.load(f)