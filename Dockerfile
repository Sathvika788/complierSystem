FROM python:3.9-slim

WORKDIR /app

# Install dependencies safely
RUN apt-get update && apt-get install -y \
    gcc g++ \
    default-jdk \
    curl \
    python3-dev \
    make \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js properly (Debian Trixie nodejs is broken)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs

# Install Go manually (Debian Trixie repo breaks)
RUN curl -LO https://golang.org/dl/go1.21.1.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go1.21.1.linux-amd64.tar.gz && \
    rm go1.21.1.linux-amd64.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"

# Install Rust the correct way
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
