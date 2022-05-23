
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
local_url = 'http://localhost:8000'

# app title and description
st.header('AI Workout Assistant')

# user upload
video_file_buffer = st.file_uploader('Choose a file')
video_file = open(video_file_buffer,'rb')
video_bytes = video_file.read()

if video_bytes is not None:
    st.video(video_bytes, caption='Video you uploaded')
    request_url = f"{local_url}/pose_video"
    if requests.post(request_url, files={'file': video_bytes}).status_code == 200:
        with st.spinner('Wait for it...'):
            response = requests.post(request_url, files={'file': video_bytes})
            st.write('Please check output video.')
    else:
        st.write('Please try again.')
else:
    st.write('AI failed to read your video.')
