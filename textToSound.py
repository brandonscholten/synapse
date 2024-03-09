import streamlit as st
from gtts import gTTS
import os

def text_to_speech(text):
    # Generate the TTS audio
    tts = gTTS(text)
    # Save the audio to a temporary file
    tts.save("temp_audio.mp3")
    # Play the audio
    st.audio("temp_audio.mp3", format="audio/mp3")

# Streamlit app
def main():
    st.title("Text-to-Speech App")

    # Text input
    text_input = st.text_input("Enter text to convert to speech")

    # Button to trigger TTS
    if st.button("Convert to Speech"):
        if text_input:
            text_to_speech(text_input)
        else:
            st.warning("Please enter some text first.")

if __name__ == "__main__":
    main()
