# Wyoming Vietnamese ASR Add-on - Minimal build
ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base:latest
FROM ${BUILD_FROM}

# Set working directory
WORKDIR /app

# Copy only required files (no pip install at build time)
COPY server/ ./server/
COPY download_model.py /app/download_model.py
COPY requirements.txt /app/requirements.txt
COPY run.sh /run.sh

RUN chmod a+x /run.sh
  # Install pip before installing dependencies
RUN apk add --no-cache python3 py3-pip && \
    pip install --no-cache-dir -r /app/requirements.txt
# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
# Install sherpa_onnx manually if pip install fails
RUN git clone https://github.com/k2-fsa/sherpa && \
    cd sherpa && \
    pip install .
RUN pip install huggingface_hub
# Create data directory for models
RUN mkdir -p /config

EXPOSE 10300 8090

# Use s6-overlay as init system (required by HA add-ons)
ENTRYPOINT ["/init"]
CMD ["/run.sh"]
