# TrueNAS API Proxy Add-on

This add-on provides a local HTTP proxy to the TrueNAS Scale WebSocket API, allowing Home Assistant integrations to communicate with TrueNAS without dealing with WebSocket directly.

## Features

- Exposes TrueNAS WebSocket API over HTTP/REST
- Supports all major TrueNAS methods: system, pool, disk, service, network, apps, containers, VMs
- Handles authentication via API key
- Runs in isolated container with minimal dependencies

## Configuration

| Option | Description |
|--------|-------------|
| `truenas_host` | TrueNAS IP or hostname (e.g., `192.168.100.198`) |
| `truenas_port` | WebSocket port (default `443` for wss) |
| `truenas_use_ssl` | Use SSL (`wss`) or plain `ws` (default `true`) |
| `truenas_verify_ssl` | Verify SSL certificate (default `false` for self-signed) |
| `truenas_api_key` | TrueNAS API key (from System → API Keys) |
| `listen_port` | Port this add-on listens on (default `8080`) |

## Usage in Home Assistant

After installing the add-on, configure your TrueNAS integration to use:

- **Host:** `http://<homeassistant-host>:8080` (or the add-on's hostname `http://truenas-api:8080` if using Supervisor network)
- The integration will send HTTP requests to this add-on, which proxies them to TrueNAS via WebSocket.

### Example curl test:

```bash
curl http://homeassistant:8080/api/v2.0/system/version
```

## Installation via HACS

1. Ensure HACS is installed.
2. Add this repository as a custom repository in HACS.
3. Install "TrueNAS API Proxy" add-on.
4. Configure with your TrueNAS details.
5. Restart the add-on.

## Building locally

```bash
git clone https://github.com/gnolnos/hassos-apps.git
cd hassos-apps/truenas_api
hassbian-build or docker build -t truenas-api .
```

## Notes

- This add-on uses the official `truenas_api_client` library (TS-25.10.2).
- Ensure your TrueNAS API key has appropriate privileges (read/write as needed).
- The proxy does not cache; it forwards each request immediately.
