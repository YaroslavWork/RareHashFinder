FROM python:3.13

WORKDIR /rare-hash-finder

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY config.yml .

CMD ["python", "./main.py"]