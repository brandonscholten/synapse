import streamlit as st
from streamlit_option_menu import option_menu
import subprocess
from st_pages import Page, Section, show_pages, add_page_title, hide_pages

#add_page_title()
show_pages(
    [
        Page("pages/main.py", "Home"),
        Page("pages/login.py", "Login"),
        Page("pages/signup.py", "Sign Up"),
    ]
)
hide_pages(["Login", "Sign Up", "Home"])

def main():
    #st.session_state.tryArray.append("Hello")
    #print(st.session_state.tryArray)
    # Read the username from the file
    try:
        with open("user_data.txt", "r") as file:
            username = file.readline()
            if username:
                st.title(f"{st.session_state.username}'s Home Page")
                # Add your main page content here
            else:
                st.warning("Please sign up first.")
    except FileNotFoundError:
        st.warning("Please sign up first.")

with st.sidebar:
        selected = option_menu(
            menu_title= "course list",
            options= ["Home", "Domain Expansion", "The Shibuya Incident", "Nanami's beach"],
        )

if selected == "Domain Expansion":
    subprocess.run(["streamlit", "run", "Domain-Expansion.py"])

elif selected == "The Shibuya Incident":
    subprocess.run(["streamlit", "run", "The-Shibuya-Incident.py"])

elif selected == "Nanami's beach":
    subprocess.run(["streamlit", "run", "Nanami-beach.py"])

    
if __name__ == "__main__":
    main()
    st.write("Welcome to your homepage! Here is this week's to-do's. be sure to navigate to your courses to take notes!")