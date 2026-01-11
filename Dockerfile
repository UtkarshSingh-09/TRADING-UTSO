# Use Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /code

# Install system dependencies (needed for some AI libs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Hugging Face Spaces run on port 7860 by default
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]