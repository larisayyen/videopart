FROM python:3.8.6-buster

WORKDIR /videopart

RUN pip install python-multipart
RUN apt-get update
RUN apt install -y libgl1-mesa-glx

COPY requirements.txt /videopart/requirements.txt
RUN pip install python-multipart
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY api/fast.py /videopart/api/fast.py
COPY videopart /videopart/videopart
COPY body_5-poses_.pkl /videopart/body_5-poses_.pkl
# COPY credentials.json /videopart/credentials.json

CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
