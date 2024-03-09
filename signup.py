# signup.py
import streamlit as st
import subprocess

def main():
    st.title("Sign Up")

    # Get user input
    username = st.text_input("Enter your username:")
    password = st.text_input("Set your password:", type="password")

    if st.button("Sign Up"):
        # Save user data or perform signup logic here

        # Run the main app with the provided username
        subprocess.run(["streamlit", "run", "main.py", f"--username={username}"])

if __name__ == "__main__":
    main()