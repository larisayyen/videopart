FROM python:3.8.6-buster

WORKDIR /videopart

COPY requirements.txt /videopart/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY api/fast.py /videopart/api/fast.py
COPY aiworkout /videopart/videopart
# COPY model.joblib /aiworkout/model.joblib
COPY credentials.json /videopart/credentials.json

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
