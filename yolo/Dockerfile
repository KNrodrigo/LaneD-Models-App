FROM nvidia/cudagl:11.4.1-devel-ubuntu20.04

# Install Python and other necessary dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y curl vim && \
    pip3 install --upgrade pip

# Set the working directory in the container
WORKDIR /app

# Copy the local files to the container
COPY . /app

# Install Python dependencies
RUN pip3 install -r requirements.txt

EXPOSE 5000

# Starting the container as the model scripts are run as standalone
CMD [ "python3", "demo.py" ]
