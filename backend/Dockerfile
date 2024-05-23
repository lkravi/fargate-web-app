# Use the official image as a parent image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Download the SSL certificate bundle and install wget
RUN apt-get update && apt-get install -y wget && \
    wget https://truststore.pki.rds.amazonaws.com/us-east-1/us-east-1-bundle.pem -O /app/us-east-1-bundle.pem && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 5001 for the Flask app
EXPOSE 5001

# Run app.py when the container launches
CMD ["python", "app.py"]
