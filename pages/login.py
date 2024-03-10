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
            st.session_state.username = username
            st.session_state.password = password
            st.session_state.docID = doc.id
            st.session_state.session_id = 0
            st.session_state.number_of_notes = use.get("num_notes")
            st.session_state.notebook = use.get("notebook")
            switch_page("summary")
    st.error("Incorrect Username or Password")

username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:")
if st.button("Submit"):
    login()