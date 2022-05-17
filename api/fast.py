
import io
import cv2
import uvicorn
import pickle
import math as m
import numpy as np
import pandas as pd
import mediapipe as mp
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse

from videopart.video_analysis import squat_analysis,deadlift_analysis,bench_analysis,pushup_analysis,bridge_analysis,findDistance,findAngle,sendWarning

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


local_model = 'body_5-poses_.pkl'
mp_holistic = mp.solutions.holistic # Mediapipe Solutions


@app.post("/predict_video")
async def predict_v(file:UploadFile = File(...)):

    contents = await file.read()

    with open(file.filename,'wb') as f:
        f.write(contents)

    vid = cv2.VideoCapture(file.filename)
    _, frame = vid.read()

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        results = holistic.process(frame)

        pose = results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

        x_pred = pd.DataFrame(pose_row)
        x_pred = x_pred.T.to_numpy()

        model = pickle.load(open(local_model,"rb"))
        y_pred = model.predict(x_pred[0].reshape(1,132))

    return {'workout pose':y_pred[0]}

@app.post("/pose_video")
async def pose_v(file:UploadFile = File(...)):

    contents = await file.read()

    with open(file.filename,'wb') as f:
        f.write(contents)

    vid = cv2.VideoCapture(file.filename)
    _, frame = vid.read()

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:

        results = holistic.process(frame)

        pose = results.pose_landmarks.landmark
        pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())

        x_pred = pd.DataFrame(pose_row)
        x_pred = x_pred.T.to_numpy()

        model = pickle.load(open(local_model,"rb"))
        y_pred = model.predict(x_pred[0].reshape(1,132))

    if y_pred == 'squat':
        out_put = squat_analysis(vid)
        return StreamingResponse(io.BytesIO(out_put),media_type='video/mp4')
    elif y_pred == 'deadlift':
        out_put = deadlift_analysis(vid)
        return StreamingResponse(io.BytesIO(out_put),media_type='video/mp4')
    elif y_pred == 'bench':
        out_put = bench_analysis(vid)
        return StreamingResponse(io.BytesIO(out_put),media_type='video/mp4')
    elif y_pred == 'pushup':
        out_put = pushup_analysis(vid)
        return StreamingResponse(io.BytesIO(out_put),media_type='video/mp4')
    elif y_pred == 'bridge':
        out_put = bridge_analysis(vid)
        return StreamingResponse(io.BytesIO(out_put),media_type='video/mp4')
    else:
        return "Fail to read the video."
