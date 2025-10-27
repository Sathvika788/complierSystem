#!/bin/bash

echo "Installing system dependencies..."

# Update package list
sudo apt-get update

# Install compilers and runtimes
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gcc \
    g++ \
    openjdk-17-jdk \
    nodejs \
    npm \
    golang \
    rustc \
    sqlite3 \
    redis-server

echo "Dependencies installed successfully!"

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

echo "Python dependencies installed!"