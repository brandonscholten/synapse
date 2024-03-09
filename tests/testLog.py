import streamlit as st
from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("grizzdata-firebase.json")

# Create a reference to the Google post.
doc_ref = db.collection("user")

# Then get the data at that reference.
info = doc_ref.document("synaps").get().to_dict()
# Let's see what we got!
st.write("The username is: ", info.get("username"))

st.write("The password is: ", info.get("password"))