import streamlit as st
from streamlit_option_menu import option_menu
from st_pages import Page, Section, show_pages, add_page_title, hide_pages
import openai
from streamlit_extras.switch_page_button import switch_page
from streamlit_chat import message
from google.cloud import firestore
import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import json 
import time

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.pinimg.com/1200x/47/26/f1/4726f134466769d03b957290290c101f.jpg");
background-size: cover;
}}

[data-testid="stTitle"] {{
background-color: #556f9f;
}}

[data-testid="stSidebar"] {{
background-color: #556f9f;
}}

</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

#add_page_title()
show_pages(
    [
        Page("pages/main.py", "Home"),
        Page("pages/login.py", "Login"),
        Page("pages/signup.py", "Sign Up"),
        Page("pages/main.py", "Main")
    ]
)
hide_pages(["Login", "Sign Up", "Home", "main"])


fb_credentials = st.secrets["firebase"]['my_project_settings']
fb_dict = dict(fb_credentials)

with open("grizzdata-firebase.json", "w") as outfile: 
    json.dump(fb_dict, outfile)

db = firestore.Client.from_service_account_json("grizzdata-firebase.json")
doc = db.collection("user").document(st.session_state.docID)

def translation():
    openai.api_key = "API_KEY_HERE"

    def api_calling(prompt):
        completions = openai.Completion.create(
            engine="latin-1",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text
        return message

    st.title("Translate!")
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
            
    def soundtotext():
        st.title("Write a Sound file:")
        def process_audio_file(audio_file):
            # Convert audio file to wav format
            audio = AudioSegment.from_file(audio_file)
            audio.export("temp_audio.wav", format="wav")

            # Recognize speech from the audio file
            recognizer = sr.Recognizer()
            with sr.AudioFile("temp_audio.wav") as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                    return text
                except sr.UnknownValueError:
                    st.warning("Sorry, I could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from Google Speech Recognition service; {e}")

            # Streamlit app
            def play():
                st.title("Speech-to-Text from Uploaded Audio")

                # File uploader
                uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

                # Button to trigger speech recognition
                if uploaded_file is not None:
                    text = process_audio_file(uploaded_file)
                    if text:
                        st.write("Text:", text)

            if __name__ == "__main__":
                play()
    if __name__=="__soundtotext__":
        soundtotext()

    def texttosound():
        st.title("turn your text to sound")
        def text_to_speech(text):
            # Generate the TTS audio
            tts = gTTS(text)
            # Save the audio to a temporary file
            tts.save("temp_audio.mp3")
            # Play the audio
            st.audio("temp_audio.mp3", format="audio/mp3")

        # Streamlit app
        def main():
            st.title("Text-to-Speech App")

            # Text input
            text_input = st.text_input("Enter text to convert to speech")

            # Button to trigger TTS
            if st.button("Convert to Speech"):
                if text_input:
                    text_to_speech(text_input)
            else:
                st.warning("Please enter some text first.")

        if __name__ == "__main__":
            main()
    if __name__=="__texttosound__":
            texttosound()

def flashcards():
    openai.api_key = "YOUR_OPENAI_API_KEY"

    def flashcards():
        st.markdown("[Open flashcards.py](flashcards.py)")
    
    def generate_flashcard(prompt):
        completions = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,  # Adjust token length based on your requirement
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = completions.choices[0].text.strip()
        return message

    st.title("Create flashcards!")

    def get_text():
        input_text = st.text_area("Enter text here", "")
        return input_text

    def get_file_content(uploaded_file):
        file_contents = uploaded_file.read().decode("latin-1")
        return file_contents

    user_input = get_text()
    file_input = st.file_uploader("Upload a file", type=["txt", "pdf"])

    if st.button("Generate Flashcard"):
        prompt = user_input
        if file_input:
            prompt += get_file_content(file_input)

        if prompt:
            flashcard = generate_flashcard(prompt)
            st.write(flashcard)


def summary():
    ###

    ## Key goes here
    openai.api_key = ""

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
        option = st.selectbox(
            'Select a current Notebook',
            (
                doc.get().to_dict()
            )
        )

        st.write('You selected:', option)
        st.session_state.choosen_notebook = option
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
                f"{st.session_state.choosen_notebook}.note{st.session_state.number_of_notes}": st.session_state.user_input,
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


def quiz():
    openai.api_key = "YOUR_API_KEY"

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

    st.title("Create a Quiz!")
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


def pomodoro_timer(work_time, break_time):
    work_seconds = work_time * 60
    break_seconds = break_time * 60

    work_placeholder = st.empty()
    break_placeholder = st.empty()

    work_placeholder.write("Work!")
    for i in range(work_seconds):
        time.sleep(1)
        work_placeholder.write(f"{work_seconds-i} seconds left")

    break_placeholder.write("Break!")
    for i in range(break_seconds):
        time.sleep(1)
        break_placeholder.write(f"{break_seconds-i} seconds left")

def make_notebook(): 
    st.session_state["notebook"] = Notebook()
    st.session_state["notebook"].title = st.session_state['notebook_title']
    st.session_state['note_id'] += 1
    st.session_state.NOTEBOOKS.append(st.session_state["notebook"])
    doc.update({
        f"{st.session_state['notebook_title']}": {}
    })

def new_notebook():
    # create a new notebook
    # show an alert to get info from the user
    #modal = Modal("",key="")
    with st.form("notebook_name"):
        #st.session_state["notebook_title"] = 
        st.text_input("title", key='notebook_title')
        st.form_submit_button("Ok", on_click=make_notebook)

#classes for notebook and class
class Notebook:
    title = "New Notebook"
    notes = []
    num_notes = 1
    total = st.session_state.number_of_notes

    def set_note(self):
        st.session_state["note"] = Note()
        notebook_data = doc.get().to_dict()
        st.session_state["note"].title = st.session_state['note_title']
        st.session_state["note_id"] += 1
        first_note = notebook_data.get(f"{st.session_state['notebook_title']}", {"note1"})
        st.session_state["note"].note = "No note found"
        st.session_state["note"].note = first_note
        self.notes.append(st.session_state["note"])
        self.num_notes += 1


    def view(self):
        st.session_state["note"] = Note()
        notebook_data = doc.get().to_dict()
        st.session_state["note"].title = st.session_state['note_title']
        st.session_state["note_id"] += 1
        first_note = notebook_data.get("notebook")
        st.session_state["note"].note = "No note found"
        st.session_state["note"].note = first_note.get("note1")[0]
        self.notes.append(st.session_state["note"])
        self.num_notes += 1
        st.title(self.title)
        st.button("new", use_container_width=True, on_click=self.new_note)
        #note cards go here
        for i in self.notes: i.view()

    def make_note(self):
        st.session_state["note"] = Note()
        st.session_state["note"].title = st.session_state['note_title']
        st.session_state["note_id"] += 1
        self.notes.append(st.session_state["note"])

    def new_note(self):
        with st.form("note_name"):
            st.text_input("title", key="note_title")
            st.form_submit_button("Ok", on_click=self.make_note)

class Note: 
    title = "New Note"
    note = "new note"
    def view(self):
        with st.container():
            st.title(self.title)
            self.note = st.text_area("contents",self.note)

# Main function to create the Streamlit app
def main():
    
    st.markdown('<style>div.Widget.row-widget.stTitle { background-color: #7795CB; }</style>', unsafe_allow_html=True)
    page = st.sidebar.radio("Select a page", [f"{st.session_state.username}'s Homepage", "Flashcards", "Summary", "Quiz", "Translation"])

    if page == f"{st.session_state.username}'s Homepage":
        st.title(f"{st.session_state.username}'s Home Page")
    elif page == "Flashcards":
        flashcards()
    elif page == "Summary":
        summary()
    elif page == "Quiz":
        quiz()
    elif page== "Translation":
        translation()
    if "NOTEBOOKS" not in st.session_state:
        print("overwriting session state")
        st.session_state["NOTEBOOKS"] = [] #list of all the ["NOTEBOOKS"] in memory
    
    if "notebook_title" not in st.session_state:
        st.session_state["notebook_title"] = ''

    if "note_id" not in st.session_state:
        st.session_state["note_id"] = 0

    if "NOTES" not in st.session_state:
        st.session_state["NOTES"] = []
    
    if "note_title" not in st.session_state:
        st.session_state["note_title"] = ""

    st.sidebar.button("new notebook", on_click=new_notebook)
    for i in st.session_state.NOTEBOOKS:
        st.sidebar.button(i.title, on_click=(i.view), key=st.session_state["note_id"]-st.session_state.NOTEBOOKS.index(i))

    #add pomodoro
    st.sidebar.subheader("Pomodoro Timer")
    work_time = st.sidebar.slider("Work Time (minutes)", 5, 90, 25)
    break_time = st.sidebar.slider("Break Time (minutes)", 1, 30, 5)

    if st.sidebar.button("Start Timer"):
        pomodoro_timer(work_time, break_time)

    if st.sidebar.button("Log out"):
        switch_page("login")
        


    # Add a navigation bar

# Run the Streamlit app
if __name__ == "__main__":
    main()