#this is fine
import streamlit as st
import openai
from streamlit_chat import message
from google.cloud import firestore
import json 


###SETS up firebase
fb_credentials = st.secrets["firebase"]['my_project_settings']
fb_dict = dict(fb_credentials)

with open("grizzdata-firebase.json", "w") as outfile: 
    json.dump(fb_dict, outfile)

db = firestore.Client.from_service_account_json("grizzdata-firebase.json")
doc = db.collection("user").document(f"{st.session_state.docID}")

###

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

st.title("Ask me anything!")
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
    prompt = user_input + file_input
    output = api_calling(prompt)
    output = output.lstrip("\n")

    # Store the output
    st.session_state.openai_response.append(prompt)
    st.session_state.user_input.append(output)
    st.session_state.number_of_notes += 1
    doc.update({
            f"notebook.note{st.session_state.number_of_notes}": st.session_state.user_input,
            "num_notes": firestore.Increment(1),
            "id": st.session_state.session_id
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
