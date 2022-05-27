
import streamlit as st
import requests

# set page tab display
st.set_page_config(
   page_title="Workout",
   page_icon= ':heart:',
   layout="wide",
   initial_sidebar_state="expanded",
)

# hide menu button
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

# API call references
base_url = 'replace with new url'
local_url = 'http://127.0.0.1:8000'

# app title and description
st.header('iworkout video')

# user upload
video_file_buffer = st.file_uploader('Choose a file', accept_multiple_files=True)

if video_file_buffer:
    video_bytes = video_file_buffer[0]

    request_url = f"{local_url}/predict_video"
    # if requests.post(request_url, files={'file': video_bytes}).status_code == 200:
    with st.spinner('Wait for it...'):
        pose = requests.post(request_url, files={'file': video_bytes}).json().get('workout pose')
        if pose:
            st.write(f'Your workout pose is: {pose}.')
        else:
            st.write('Please try again.')
