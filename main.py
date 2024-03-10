import copy
import streamlit as st
from streamlit_modal import Modal

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
    def view(): print("works")

class Note: 
    title = "New Note"
    note = ""

def make_notebook(): #TODO: name is not being passed correctly
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
                st.sidebar.button(i.title, on_click=print, args=("success", ), key=st.session_state["note_id"]-st.session_state.NOTEBOOKS.index(i))
    

# Run the Streamlit app
if __name__ == "__main__":
    main()

st.write("This is the homepage. Choose a page from the navigation bar.")
