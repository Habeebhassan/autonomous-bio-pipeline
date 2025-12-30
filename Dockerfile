# Use a lightweight Python version suitable for data science
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definition first (caching layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command (can be overridden)
CMD ["python", "main.py"]