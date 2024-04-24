# official Python base image
FROM python:3

# Install Python dependencies
RUN pip3 install -r requirements.txt

# working directory 
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port on which Flask will run (default is 5000)
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "app.py"]
