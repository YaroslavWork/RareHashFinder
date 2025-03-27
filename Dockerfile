FROM python:3.13

WORKDIR /rare-hashes-website

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY config.yml .

CMD ["python", "./main.py"]