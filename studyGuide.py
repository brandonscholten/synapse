import streamlit as st
import openai
from streamlit_chat import message

openai.api_key = "YOUR_API_KEY"

def api_calling(prompt):
    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

st.title("Create a study guide!")
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
