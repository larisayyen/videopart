
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
st.header('iworkout video')

# user upload
video_file_buffer = st.file_uploader('Choose a file', accept_multiple_files=True)

if video_file_buffer:

    video_bytes = video_file_buffer[0].getvalue()

    #video pose prediction

    predict_url = f'{local_url}/predict_video'

    with st.spinner('Wait for it...'):
        pose = requests.post(predict_url, files={'file': video_bytes}).json()
        pose_name = pose.get('workout pose')

        if pose_name:
            st.write(f'Your workout pose is: {pose_name}.')

            option = st.selectbox('Is that correct?', ('-', 'Yes', 'No'))

            if option == 'No':
                pose = st.radio('Please choose your pose for scoring',
                                ('bench', 'deadlift', 'squat', 'bridge', 'pushup'))

                option = 'Yes'

            #video annotation

            if option == 'Yes':
                with st.spinner('Wait for it...'):
                    request_url = f'{local_url}/pose_video'
                    pose_video = requests.post(request_url, files={'file': video_bytes},stream = True).content
                    # st.video(pose_video)

        else:
            st.write('Sorry. AI failed to read your video.')
