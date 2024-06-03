FROM nvidia/cudagl:11.4.1-devel-ubuntu20.04

# Install Python and other necessary dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    curl \
    vim && \
    pip3 install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container, i did this to speed up image build process
COPY requirements.txt /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Expose the container port for the flask server
EXPOSE 5000

# Starting the container as the model scripts are run as standalone
CMD [ "python3", "demo.py" ]
