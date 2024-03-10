import streamlit as st
from streamlit_extras.switch_page_button import switch_page

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
background-image: url("https://i.pinimg.com/1200x/47/26/f1/4726f134466769d03b957290290c101f.jpg");
background-size: cover;
}}


</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

st.title("Synapsify")

if st.button("Sign Up"):
    switch_page("signup")
if st.button("Login"):
    switch_page("login")