FROM python:3.11-alpine3.20

WORKDIR /tributary

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "entrypoint:app"]