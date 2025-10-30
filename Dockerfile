# Use Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy your Flask app
COPY app.py /app

# Install Flask
RUN pip install flask

# Command to run your app
CMD ["python", "app.py"]
