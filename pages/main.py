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
    ]
)
hide_pages(["Login", "Sign Up", "Home"])

def domain_expansion():
    st.title("Domain Expansion Page")
    st.write("This is the Domain Expansion page content.")

# Function to display The Shibuya Incident page content
def shibuya_incident():
    st.title("The Shibuya Incident Page")
    st.write("This is The Shibuya Incident page content.")

# Function to display Nanami's Beach page content
def nanamis_beach():
    st.title("Nanami's Beach Page")
    st.write("This is Nanami's Beach page content.")

def main():
    #st.session_state.tryArray.append("Hello")
    #print(st.session_state.tryArray)
    # Read the username from the file
    try:
        with open("user_data.txt", "r") as file:
            username = file.readline()
            if username:
                st.title(f"{st.session_state.username}'s Home Page")
                st.markdown('<style>div.Widget.row-widget.stTitle { background-color: #7795CB; }</style>', unsafe_allow_html=True)
                st.write("Welcome to your homepage! Here is this week's to-do's. be sure to navigate to your courses to take notes!")
                page = st.sidebar.radio("Select a page", [f"{st.session_state.username}'s Homepage", "Domain Expansion", "The Shibuya Incident", "Nanami's Beach"])
            else:
                st.warning("Please sign up first.")
    except FileNotFoundError:
        st.warning("Please sign up first.")

    # with st.sidebar:
    #     selected = option_menu(
    #         menu_title= "course list",
    #         options= ["Home", "Domain Expansion", "The Shibuya Incident", "Nanami's beach"],
    #     )
        
    if page == "Domain Expansion":
        domain_expansion()
    elif page == "The Shibuya Incident":
        shibuya_incident()
    elif page == "Nanami's Beach":
        nanamis_beach()


    
if __name__ == "__main__":
    main()
    