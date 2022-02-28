FROM python:3.8-slim-buster

RUN apt-get update -y

RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN apt-get install -y wget

RUN /usr/local/bin/python -m pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt


RUN wget https://models.s3.ap-southeast-2.amazonaws.com/u2net.onnx -P models/

EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run","--host=0.0.0.0"]
