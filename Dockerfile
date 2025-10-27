FROM python:3.9-slim

WORKDIR /app

# Install system dependencies and ALL compilers
RUN apt-get update && apt-get install -y \
    gcc g++ \
    openjdk-11-jdk \
    nodejs npm \
    golang \
    rustc cargo \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]