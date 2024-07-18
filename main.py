import streamlit as st
st.set_page_config(page_title="TrialMatchAI", page_icon='/home/sharanya/AI_env/clinical_records/images/vairam1.ico', layout="centered",initial_sidebar_state="auto", menu_items=None)
import home
import Structured_Data
import Unstructured_Data
import contact
from streamlit_option_menu import option_menu
import streamlit_shadcn_ui as ui
import os
from dotenv import load_dotenv
# Define custom CSS
# custom_css = """
# <style>
#     .custom-menu-title {
#         color: black; /* Change this to your desired color */
#         font-size: 20px; /* Adjust the font size if needed */
#     }
# </style>
# """

# # Inject custom CSS
# st.markdown(custom_css, unsafe_allow_html=True)




def run():
    st.image('/home/sharanya/AI_env/pinnacle_biologics/images/3.jpg')
    st.sidebar.image("/home/sharanya/AI_env/pinnacle_biologics/images/vairam1.png", use_column_width=True)
    st.sidebar.divider()
    st.sidebar.markdown("Powered by NEURONWORKS.AI")
    ui.badges(badge_list=[("NeuronWorks.ai", "default"), ("Associated with", "secondary"), ("Vairam", "destructive")], class_name="flex gap-2", key="main_badges1")
    st.caption("Trialmatch chatbot for your clinical record related questions")
    with ui.element("div", className="flex gap-2", key="buttons_group1"):
        ui.element("button", text="Get Started", className="btn btn-primary", key="btn1")
        ui.element("link_button", text="Pinnacle Biologics", url="https://pinnaclebiologics.com/", variant="outline", key="btn2")
    if 'selected_menu' not in st.session_state:
        st.session_state['selected_menu'] = 'Home'

    selected_menu = option_menu(
        menu_title='Trial Match AI',
        options=['Home', 'Structure Data', 'Unstructure Data', 'Contact Us'],
        icons=['house', 'cloud-upload', 'cloud-upload', 'envelope'],
        menu_icon="chat-text-fill",
        default_index=['Home', 'Structure Data', 'Unstructure Data', 'Contact Us'].index(st.session_state['selected_menu']),
        orientation="horizontal",
        styles={
                "container": {"padding": "0!important", "background-color": "#E0EFEF"},
                "icon": {"color": "red", "font-size": "15px"},
                "nav-link": {"color": "black", "font-size": "15px", "text-align": "center", "margin": "0px", "--hover-color": "white"},
                "nav-link-selected": {"background-color": "#A0C8DC"},
        },
        key='selected_menu'
    )
       
    if st.session_state['selected_menu'] == 'Home':
        home.app()
    elif st.session_state['selected_menu'] == 'Structure Data':
        Structured_Data.app()
    elif st.session_state['selected_menu'] == 'Unstructure Data':
        Unstructured_Data.app()
    elif st.session_state['selected_menu'] == 'Contact Us':
        contact.app()


run()
