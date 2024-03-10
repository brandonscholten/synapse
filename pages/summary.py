#this is fine
import streamlit as st
import openai
from streamlit_chat import message
from google.cloud import firestore
import json 
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

##CSS to hide the side bar
add_page_title()
show_pages(
    [
        Page("pages/main.py", "Home"),
        Page("pages/login.py", "Login"),
        Page("pages/signup.py", "Sign Up"),
        Page("pages/summary.py", "Summary")
    ]
)
hide_pages(["Login", "Sign Up", "Home", "Summary"])
css ='''
<style>
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
'''

###SETS up firebase
fb_credentials = st.secrets["firebase"]['my_project_settings']
fb_dict = dict(fb_credentials)

with open("grizzdata-firebase.json", "w") as outfile: 
    json.dump(fb_dict, outfile)

db = firestore.Client.from_service_account_json("grizzdata-firebase.json")
doc = db.collection("user").document(st.session_state.docID)
###

## Key goes here
#openai.api_key = ""

def api_calling(prompt):
    completions = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

st.title("Create a summary!")
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
    st.session_state['openai_response'] = []

def get_text():
    input_text = st.text_input("Write here", key="input")
    return input_text

def get_file():
    uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf"])
    if uploaded_file is not None:
        file_contents = uploaded_file.read()
        return file_contents.decode("latin-1")
    else:
        return ""

user_input = get_text()
file_input = get_file()

if user_input or file_input:
    prompt = user_input + file_input + " summarize"
    output = api_calling(prompt)
    output = output.lstrip("\n")

    # Store the output
    st.session_state.openai_response.append(prompt)
    st.session_state.user_input.append(output)
    if st.session_state.session_id == 0:
        st.session_state.session_id = 1
        st.session_state.number_of_notes += 1
        st.write("In")
        doc.update({
            f"notebook.note{st.session_state.number_of_notes}": st.session_state.user_input,
            "num_notes": firestore.Increment(1),
            "id": st.session_state.session_id
        })
    else:
        st.write("out")
        doc.update({
            f"notebook.note{st.session_state.number_of_notes}": st.session_state.user_input,
        })

message_history = st.empty()

if st.session_state['user_input']:
    for i in range(len(st.session_state['user_input']) - 1, -1, -1):
        # This function displays user input
        message(st.session_state["user_input"][i], 
                key=str(i),avatar_style="icons")
        # This function displays OpenAI response
        message(st.session_state['openai_response'][i], 
                avatar_style="miniavs",is_user=True,
                key=str(i) + 'data_by_user')
