# webNUT

[English](README.md) | [简体中文](README.zh-CN.md)

webNUT is a web interface for viewing NUT UPS status.

This project is forked from [rshipp/webNUT](https://github.com/rshipp/webNUT).

Updates in this fork:

- Adds login protection.
- Adds relative detail links for reverse proxy deployments.
- Adds Docker images.

## Run

```bash
docker run -d \
  --name webnut \
  -p 6543:6543 \
  -e NUT_SERVER=127.0.0.1 \
  -e NUT_PORT=3493 \
  -e NUT_USERNAME= \
  -e NUT_PASSWORD= \
  -e WEBNUT_USERNAME=admin \
  -e WEBNUT_PASSWORD=change-me \
  heifeng/webnut:latest
```

## Configuration

At startup, webNUT reads `webnut/config.py` first, then reads environment variables. Environment variables with valid values override the file configuration.

- `NUT_SERVER`: NUT server hostname or IP address.
- `NUT_PORT`: NUT server port. Must be an integer.
- `NUT_USERNAME`: NUT username. Leave empty when the NUT server does not require authentication.
- `NUT_PASSWORD`: NUT password. Leave empty when the NUT server does not require authentication.
- `WEBNUT_USERNAME`: Basic Auth username for accessing WebNUT.
- `WEBNUT_PASSWORD`: Basic Auth password for accessing WebNUT.

Empty strings do not override the file configuration.

WebNUT protects page access with Basic Auth. You must configure `WEBNUT_USERNAME` and `WEBNUT_PASSWORD` before logging in.

## Build Images

```bash
make docker
```

The default build creates x86 images with these tags:

- `heifeng/webnut:latest`
- `heifeng/webnut:<YYYYMMDDHHMMSS>`

Build arm64 images:

```bash
make docker-arm64
```

arm64 image tags:

- `heifeng/webnut:latest-arm64`
- `heifeng/webnut:<YYYYMMDDHHMMSS>-arm64`
