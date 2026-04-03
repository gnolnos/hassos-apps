#!/usr/bin/env python3
"""HTTP proxy to TrueNAS WebSocket API for Home Assistant."""
import os
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from truenas_api_client import Client

app = Flask(__name__)
CORS(app)

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Config from env (HassOS add-on passes config as env vars)
TRUENAS_HOST = os.getenv("TRUENAS_HOST", "192.168.100.198")
TRUENAS_PORT = int(os.getenv("TRUENAS_PORT", "443"))
TRUENAS_USE_SSL = os.getenv("TRUENAS_USE_SSL", "true").lower() == "true"
TRUENAS_VERIFY_SSL = os.getenv("TRUENAS_VERIFY_SSL", "false").lower() == "true"
TRUENAS_API_KEY = os.getenv("TRUENAS_API_KEY", "")
LISTEN_PORT = int(os.getenv("LISTEN_PORT", "8080"))

class TrueNASProxy:
    def __init__(self):
        self.client = None

    def connect(self):
        if self.client is not None:
            return
        uri = f"{'wss' if TRUENAS_USE_SSL else 'ws'}://{TRUENAS_HOST}:{TRUENAS_PORT}/api/current"
        _LOGGER.info("Connecting to TrueNAS at %s", uri)
        self.client = Client(uri=uri, verify_ssl=TRUENAS_VERIFY_SSL)
        self.client.connect()
        # Login with API key (username may be empty)
        try:
            self.client.login_with_api_key("", TRUENAS_API_KEY)
            _LOGGER.info("Authenticated to TrueNAS")
        except Exception as e:
            _LOGGER.error("Authentication failed: %s", e)
            self.client.close()
            self.client = None
            raise

    def call(self, method, params=None):
        if self.client is None:
            self.connect()
        try:
            if params is None:
                result = self.client.call(method)
            else:
                result = self.client.call(method, params)
            return result
        except Exception as e:
            _LOGGER.error("RPC error %s: %s", method, e)
            raise

proxy = TrueNASProxy()

@app.route('/api/v2.0/<path:method>', methods=['GET', 'POST'])
def handle_api(method):
    # Map method from URL to RPC method
    # e.g., system/version -> system.version
    rpc_method = method.replace('/', '.')
    # Get params from JSON body (POST) or query (GET)
    if request.method == 'POST':
        if request.is_json:
            params = request.get_json()
        else:
            params = {}
    else:
        # GET: parse query string as params dict
        params = request.args.to_dict()
        # Convert numeric strings? For simplicity, treat all as strings, TrueNAS API may accept
    try:
        result = proxy.call(rpc_method, params)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    _LOGGER.info("Starting TrueNAS API proxy on port %s", LISTEN_PORT)
    app.run(host='0.0.0.0', port=LISTEN_PORT, debug=False)
