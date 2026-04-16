# Use Home Assistant base image
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Set working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/requirements.txt

# Install Python 3 and pip, then create a virtual environment and install dependencies
RUN apk add --no-cache python3 py3-pip && \
    python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy remaining application files
COPY server/ ./server/
COPY download_model.py /app/download_model.py
COPY run.sh /run.sh

# Set executable permissions for run.sh
RUN chmod +x /run.sh

# Create necessary directories
RUN mkdir -p /config

# Expose application ports
EXPOSE 10300 8090

# Start container with s6-overlay
ENTRYPOINT ["/init"]
CMD ["/run.sh"]