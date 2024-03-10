import streamlit as st
import subprocess
from streamlit_extras.switch_page_button import switch_page
from google.cloud import firestore
import json 

css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)

fb_credentials = st.secrets["firebase"]['my_project_settings']
fb_dict = dict(fb_credentials)

# Convert and write JSON object to file
with open("grizzdata-firebase.json", "w") as outfile: 
    json.dump(fb_dict, outfile)

db = firestore.Client.from_service_account_json("grizzdata-firebase.json")
doc = db.collection("user")

def signup():
    st.title("User Signup")
    username = st.text_input("Enter your username:")
    password = st.text_input("Enter your password:")

    if st.button("Submit"):
        userDict = toDict(username, password)
        doc.add(userDict)
        st.success("Signup successful!")

        # Automatically open main.py after storing the username
        switch_page("main")

def toDict(user, pas):
    return {"username": user, "password": pas }

signup()
