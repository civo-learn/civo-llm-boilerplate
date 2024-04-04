FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

COPY main.py .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

CMD ["python", "main.py"]