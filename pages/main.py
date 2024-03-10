import streamlit as st
from streamlit_option_menu import option_menu
import subprocess
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.pinimg.com/1200x/47/26/f1/4726f134466769d03b957290290c101f.jpg");
background-size: cover;
back
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
    ]
)
hide_pages(["Login", "Sign Up", "Home"])

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
        st.write('pretend there are nicely formatted notes here')
        #note cards go here

class Note: 
    title = "New Note"
    note = ""
    def view(): print("stub")


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
        print("set notebook title")
        st.form_submit_button("Ok", on_click=make_notebook)
    print(st.session_state.NOTEBOOKS)
    print(st.session_state)

# Main function to create the Streamlit app
def main():
    if "NOTEBOOKS" not in st.session_state:
        print("overwriting session state")
        st.session_state["NOTEBOOKS"] = [] #list of all the ["NOTEBOOKS"] in memory
        #st.session_state["notebook_title"] = ''
        #st.session_state["note_id"] = 0
    
    if "notebook_title" not in st.session_state:
        st.session_state["notebook_title"] = ''

    if "note_id" not in st.session_state:
        st.session_state["note_id"] = 0

    # Add a navigation bar
    with open("user_data.txt", "r") as file:
        username = file.readline()
        if username:
            st.sidebar.button("new notebook", on_click=new_notebook)
            for i in st.session_state.NOTEBOOKS:
                st.sidebar.button(i.title, on_click=(i.view), key=st.session_state["note_id"]-st.session_state.NOTEBOOKS.index(i))
    

# Run the Streamlit app
if __name__ == "__main__":
    main()