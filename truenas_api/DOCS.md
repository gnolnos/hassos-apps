# Documentation

## Architecture

The add-on runs a small Flask server that accepts HTTP requests and forwards them to TrueNAS via the official `truenas_api_client` over WebSocket.

## Adding to Home Assistant

1. Install this add-on from your custom repository.
2. Configure the add-on with your TrueNAS details.
3. Start the add-on.
4. In your Home Assistant integration (custom component), set the host to `http://truenas-api:8080` (or the IP of the add-on container).
5. Ensure the integration uses HTTP (no SSL) to talk to the add-on.

## Security

- The add-on does not implement authentication; it assumes it runs in a trusted network (Supervisor internal network).
- TrueNAS API key is stored in the add-on configuration (encrypted by Supervisor).
- Use SSL verification (`truenas_verify_ssl`) when connecting to TrueNAS if using valid certificates.

## Development

To modify:

1. Edit `server/proxy.py` for proxy logic.
2. Rebuild the add-on via Supervisor → Add-on store → Build.
3. Or build locally with `docker build`.

## Support

For issues, please open an issue on the GitHub repository.
