import streamlit as st
from google.cloud import firestore
from streamlit_extras.switch_page_button import switch_page
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
#This pulls all the current documents in the user database
docs = db.collection("user").stream()


st.write("Login Page")


def login():
    for doc in docs:
        use = doc.to_dict()
        if username == use.get("username") and password == use.get("password"):
            st.success("Signup successful!")
            switch_page("main")
    st.error("Incorrect Username or Password")

username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:")
if st.button("Submit"):
    login()