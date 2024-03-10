import streamlit as st
from streamlit_drawable_canvas import st_canvas

drawing_mode = st.selectbox(
    "Drawing tool:",
    ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
)
stroke_width = st.slider("Stroke width: ", 1, 25, 3)
if drawing_mode == "point":
    point_display_radius = st.slider("Point display radius: ", 1, 25, 3)
stroke_color = st.color_picker("Stroke color hex: ")
bg_color = st.color_picker("Background color hex: ", "#eee")
realtime_update = st.checkbox("Update in realtime", True)

# Create a canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    update_streamlit=realtime_update,
    height=800,
    drawing_mode=drawing_mode,
    point_display_radius=point_display_radius if drawing_mode == "point" else 0,
    display_toolbar=st.checkbox("Display toolbar", True),
    key="full_app",
)

