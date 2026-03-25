#!/bin/bash
set -e

CONFIG_PATH=/data/options.json

# Read configuration
LOG_LEVEL=$(jq --raw-output '.log_level // "info"' "$CONFIG_PATH")
EXTERNAL_MODEL_PATH=$(jq --raw-output '.external_model_path // "/config/model"' "$CONFIG_PATH")

# Set log level
export RUST_LOG="${LOG_LEVEL}"
export LOG_LEVEL="${LOG_LEVEL}"

# Set model path (default: /config/model)
export MODEL_PATH="${EXTERNAL_MODEL_PATH}"

echo "====================================="
echo "🧠 Wyoming Vietnamese ASR Add-on"
echo "====================================="
echo "Model: hynt/Zipformer-30M-RNNT-6000h"
echo "Log level: ${LOG_LEVEL}"
echo "Model path: ${MODEL_PATH}"
echo "====================================="

# Install system dependencies (Alpine) - idempotent
echo "📦 Ensuring system dependencies..."
apk add --no-cache python3 py3-pip bash jq ffmpeg libsndfile || true

# Install Python packages (first run only)
echo "🔧 Installing Python packages..."
pip3 install --no-cache-dir --break-system-packages \
    wyoming==1.5.0 \
    soundfile==0.12.1 \
    fastapi==0.104.1 \
    uvicorn==0.24.0 \
    huggingface-hub==0.20.3 \
    sherpa_onnx==1.12.29 || true

# Ensure model directory exists
mkdir -p "${MODEL_PATH}"

# Download model if not present
echo "🔽 Checking model files in ${MODEL_PATH}..."
python3 /app/download_model.py

# Change to app directory
cd /app

# Start Wyoming server
echo "🚀 Starting server..."
python3 server/main.py
