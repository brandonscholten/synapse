import streamlit as st
from streamlit_option_menu import option_menu
import subprocess
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.pinimg.com/1200x/47/26/f1/4726f134466769d03b957290290c101f.jpg");
background-size: cover;
}}

[data-test="stHeading"] > .main{{
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
        Page("pages/summary.py", "Summary")
    ]
)
hide_pages(["Login", "Sign Up", "Home", "Summary"])

def make_notebook(): 
    st.session_state["notebook"] = Notebook()
    st.session_state["notebook"].title = st.session_state['notebook_title']
    st.session_state['note_id'] += 1
    st.session_state.NOTEBOOKS.append(st.session_state["notebook"])

def new_notebook():
    # create a new notebook
    # show an alert to get info from the user
    #modal = Modal("",key="")
    with st.form("notebook_name"):
        #st.session_state["notebook_title"] = 
        st.text_input("title", key='notebook_title')
        st.form_submit_button("Ok", on_click=make_notebook)

# Function to display the homepage content
def homepage():
    with open("user_data.txt", "r") as file:
        username = file.readline()
        if username:
            st.title(f"{username}'s Home Page")

#classes for notebook and class
class Notebook:
    title = "New Notebook"
    notes = []
    def view(self): 
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
    page = st.sidebar.radio("Select a page", [f"{st.session_state.username}'s Homepage", "Domain Expansion", "The Shibuya Incident", "Nanami's Beach"])

    if page == f"{st.session_state.username}'s Homepage":
        st.title(f"{st.session_state.username}'s Home Page")
    elif page == "Domain Expansion":
        print("hello")
    elif page == "The Shibuya Incident":
        print("hello")
    elif page == "Nanami's Beach":
        print("hello")

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

    # Add a navigation bar

    st.sidebar.button("new notebook", on_click=new_notebook)
    for i in st.session_state.NOTEBOOKS:
    	st.sidebar.button(i.title, on_click=(i.view), key=st.session_state["note_id"]-st.session_state.NOTEBOOKS.index(i))

# Run the Streamlit app
if __name__ == "__main__":
    main()