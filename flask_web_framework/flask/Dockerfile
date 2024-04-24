# official Python base image
FROM python:3.9-slim

# working directory 
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install Flask

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Expose the port on which Flask will run (default is 5000)
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
