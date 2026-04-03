ARG BUILD_FROM=ghcr.io/hassio-addons/base:14.0.0
FROM ${BUILD_FROM}

# Install python3 and pip
RUN apk add --no-cache python3 py3-pip

# Install truenas_api_client from git
RUN pip3 install --no-cache-dir git+https://github.com/truenas/api_client.git@TS-25.10.2

# Copy our proxy server
COPY server/ /usr/src/truenas_api/
WORKDIR /usr/src/truenas_api

# Install Flask for HTTP proxy
RUN pip3 install --no-cache-dir flask flask-cors

EXPOSE 8080

CMD ["python3", "proxy.py"]
