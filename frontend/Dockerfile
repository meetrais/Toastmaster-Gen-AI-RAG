FROM python:3.8-slim

WORKDIR /usr/src/app
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . .
EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["python", "app.py"]