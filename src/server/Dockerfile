FROM python:3.8

LABEL authors="P3TER"

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

ADD . /app

CMD ["uvicorn", "server_main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
