FROM python:3.12-slim

WORKDIR /app

COPY car-rent/backend/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY car-rent/backend/ ./

EXPOSE 5000

CMD ["python", "app.py"]