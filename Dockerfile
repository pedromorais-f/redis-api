FROM python:3.10.12

WORKDIR /app

COPY . .

ENV PYTHONPATH "${PYTHONPATH}:/app/"

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


EXPOSE 6379