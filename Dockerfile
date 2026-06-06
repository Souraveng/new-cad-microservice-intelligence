FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic python-multipart

# Copy the microservice source code
COPY . .

# Cloud Run defaults to exposing port 8080
ENV PORT=8080
EXPOSE 8080

CMD ["python", "main.py"]
