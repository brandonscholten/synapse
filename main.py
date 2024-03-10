
import streamlit as st

# Function to display the homepage content
def homepage():
    with open("user_data.txt", "r") as file:
        username = file.readline()
        if username:
            st.title(f"{username}'s Home Page")
    

# Function to display the Domain Expansion page content
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

# Main function to create the Streamlit app
def main():


    # Add a navigation bar
    with open("user_data.txt", "r") as file:
        username = file.readline()
        if username:
            page = st.sidebar.radio("Select a page", [f"{username}'s Homepage", "Domain Expansion", "The Shibuya Incident", "Nanami's Beach"])

    # Display the selected page
    if page == f"{username}'s Homepage":
        homepage()
    elif page == "Domain Expansion":
        domain_expansion()
    elif page == "The Shibuya Incident":
        shibuya_incident()
    elif page == "Nanami's Beach":
        nanamis_beach()

# Run the Streamlit app
if __name__ == "__main__":
    main()

st.write("This is the homepage. Choose a page from the navigation bar.")
