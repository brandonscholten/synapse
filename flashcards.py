#This will need to be refined better
import streamlit as st
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

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
