# main.py
import streamlit as st
import sys

def main():
    # Get the username from command-line arguments
    username = st.experimental_get_query_params().get("username", [None])[0]

    if username is not None:
        st.title(f"{username}'s Home Page")
        # Add your main page content here

if __name__ == "__main__":
    main()
