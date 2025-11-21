FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies and ALL compilers
RUN apt-get update && apt-get install -y \
    gcc g++ \
    default-jdk \
    nodejs npm \
    golang \
    rustc cargo \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

# Expose API port
EXPOSE 8000

# Start FastAPI server
CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
