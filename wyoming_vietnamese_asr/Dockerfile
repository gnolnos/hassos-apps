# Use Home Assistant base image
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Set working directory
WORKDIR /app

# Install Python 3 and pip, then create a virtual environment for the application
RUN apk add --no-cache python3 py3-pip && \
    python3 -m venv /app/venv && \
    . /app/venv/bin/activate && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy application files into the container
COPY server/ ./server/
COPY download_model.py /app/download_model.py
COPY requirements.txt /app/requirements.txt
COPY run.sh /run.sh

# Set executable permissions for the run script
RUN chmod +x /run.sh

# Create necessary directories
RUN mkdir -p /config

# Expose application ports
EXPOSE 10400 8090

# Start container with s6-overlay
ENTRYPOINT ["/init"]
CMD ["/run.sh"]