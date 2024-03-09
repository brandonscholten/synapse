#fine tune this if we have time
import streamlit as st
import time

# Pomodoro Timer Function
st.title("Streamlit Pomodoro Timer")

work_time= st.slider("Work Time (minutes)", 5, 90, 25)
break_time= st.slider("Break Time (minutes)", 1, 30, 5)

def pomodoro_timer(work_time, break_time):
    work_seconds= work_time*60
    break_seconds= break_time*60

    work_placeholder=st.empty()
    breakplaceholder=st.empty()

    work_placeholder.write("Work!")
    for i in range(work_seconds):
        time.sleep(1)
        work_placeholder.write(f"{work_seconds-i} seconds left")

    breakplaceholder.write("Break!")
    for i in range(break_seconds):
        time.sleep(1)
        breakplaceholder.write(f"{break_seconds-i} seconds left")

if st.button("Start Timer"):
    pomodoro_timer(work_time, break_time)
