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
copyDoc = db.collection("user").stream()

def signup():
    st.title("User Signup")
    #st.session_state.tryArray = []
    st.session_state.username = st.text_input("Enter your username:")
    taken = False
    for cDoc in copyDoc:
        use = cDoc.to_dict()
        if(st.session_state.username == use.get("username")):
            taken = True
            st.error("Username is taken")
            break
    st.session_state.password = st.text_input("Enter your password:")
    st.session_state.number_of_notes = 0
    st.session_state.notebook = {"title":""}
    

    if st.button("Submit") and not taken:
        userDict = toDict(st.session_state.username, st.session_state.password, st.session_state.number_of_notes, st.session_state.notebook, "")
        update_time, doc_ref = doc.add(userDict)
        st.session_state.docID = doc_ref.id
        st.session_state.session_id = 0
        st.success("Signup successful!")
        # Automatically open main.py after storing the username
        switch_page("summary")

def toDict(user, pas, num_notes, notebook, id):
    return {"username": user, "password": pas, "num_notes": num_notes, "notebook": notebook, "id": id }

signup()
