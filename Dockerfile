# Base image with Python 3.12
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files in the current directory to the working directory in the container
COPY . /app

# Install any required packages (update with dependencies if you have them)
RUN pip install --no-cache-dir -r requirements.txt || true

# Run the IMS.py file when the container starts
CMD ["python", "IMS.py"]
