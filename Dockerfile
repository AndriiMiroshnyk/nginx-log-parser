FROM python:3.12-slim

WORKDIR /app

COPY nginx_to_csv.py .

ENTRYPOINT ["python", "nginx_to_csv.py"]