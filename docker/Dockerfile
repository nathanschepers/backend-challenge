FROM python:3.10.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY .env.sh .env.sh
COPY docker/entrypoint.sh entrypoint.sh
COPY dal/ ./dal
COPY ecg/ ./ecg
COPY tests/ ./tests
COPY app.py app.py
COPY init.py init.py

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["echo", "Hello, world!"]
