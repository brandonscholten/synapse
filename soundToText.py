import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
import os

def process_audio_file(audio_file):
    # Convert audio file to wav format
    audio = AudioSegment.from_file(audio_file)
    audio.export("temp_audio.wav", format="wav")

    # Recognize speech from the audio file
    recognizer = sr.Recognizer()
    with sr.AudioFile("temp_audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.warning("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")

# Streamlit app
def main():
    st.title("Speech-to-Text from Uploaded Audio")

    # File uploader
    uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])

    # Button to trigger speech recognition
    if uploaded_file is not None:
        text = process_audio_file(uploaded_file)
        if text:
            st.write("Text:", text)

if __name__ == "__main__":
    main()
