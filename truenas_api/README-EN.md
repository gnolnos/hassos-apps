# TrueNAS API Proxy Add-on

Provides an HTTP-to-WebSocket proxy for TrueNAS Scale API, enabling Home Assistant to interact with TrueNAS using simple HTTP calls.

## Configuration Options

- **truenas_host**: TrueNAS server address (e.g., `192.168.100.198`)
- **truenas_port**: WebSocket port (usually `443` for secure, `80` for plain)
- **truenas_use_ssl**: Enable SSL (`wss://`) (default: `true`)
- **truenas_verify_ssl**: Verify SSL certificate (default: `false` for self-signed)
- **truenas_api_key**: API key generated in TrueNAS (System → API Keys)
- **listen_port**: Local port to listen on (default: `8080`)

## Networking

The add-on listens on all interfaces (`0.0.0.0`). Home Assistant can reach it via:

- If both are on the same Supervisor network: `http://truenas-api:8080`
- If HA is on the host: `http://homeassistant:8080` (or IP of the add-on container)

## API Endpoints

All TrueNAS methods are available under `/api/v2.0/...` using REST-like mapping:

- `GET /api/v2.0/system/version` → calls `system.version`
- `POST /api/v2.0/pool` with JSON body → calls `pool.query` (params from body)
- `GET /api/v2.0/disk?ids=...` → passes query params as RPC params

Essentially, any JSON-RPC method can be called by converting `/` to `.` in the URL path.

## Example

```bash
curl http://truenas-api:8080/api/v2.0/system/version
# {"version": "25.10.0"}
```

## Troubleshooting

- Check add-on logs via Supervisor → Add-ons → TrueNAS API Proxy → Logs.
- Ensure TrueNAS host is reachable from the add-on container (ping test).
- Verify API key permissions in TrueNAS (needs at least READ access).
- If SSL errors occur, set `truenas_verify_ssl: false`.
