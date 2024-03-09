# main.py
# import streamlit as st
# import sys

# def main():
#     # Get the username from query parameters
#     query_params = st.url_context.request.query_params
#     username = query_params.get("username", [None])[0]

#     if username is not None:
#         st.title(f"{username}'s Home Page")
#         # Add your main page content here

# if __name__ == "__main__":
#     main()

#------------------------------------------------------
# # main.py
# import streamlit as st

# def main():
#     st.title("Main Page")
    
#     # Read the username from the file
#     try:
#         with open("user_data.txt", "r") as file:
#             username = file.read()
#             if username:
#                 st.title(f"{username}'s Home Page")
#                 # Add your main page content here
#             else:
#                 st.warning("Please sign up first.")
#     except FileNotFoundError:
#         st.warning("Please sign up first.")

# if __name__ == "__main__":
#     main()

import streamlit as st
from streamlit_option_menu import option_menu
import subprocess

def main():
    
    # Read the username from the file
    try:
        with open("user_data.txt", "r") as file:
            username = file.readline()
            if username:
                st.title(f"{username}'s Home Page")
                # Add your main page content here
            else:
                st.warning("Please sign up first.")
    except FileNotFoundError:
        st.warning("Please sign up first.")

st.write("Welcome to your homepage! Here is this week's to-do's. be sure to navigate to your courses to take notes!")

with st.sidebar:
        selected = option_menu(
            menu_title= "course list",
            options= ["Domain Expansion", "The Shibuya Incident", "Nanami's beach"],
        )
if selected == "Domain Expansion":
        subprocess.run(["streamlit", "run", "Domain Expansion.py"])

elif selected == "The Shibuya Incident":
        subprocess.run(["streamlit", "run", "The Shibuya Incident.py"])

elif selected == "Nanami's beach":
        subprocess.run(["streamlit", "run", "Nanami's beach.py"])

    
if __name__ == "__main__":
    main()



