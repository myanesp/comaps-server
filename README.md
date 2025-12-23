# CoMaps map Docker server

[![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/myanesp/comaps-server)
[![Last Commit](https://img.shields.io/github/last-commit/myanesp/comaps-server)](https://github.com/myanesp/comaps-server)
[![Docker Image Size](https://badgen.net/docker/size/myanesp/comaps-server?icon=docker&label=image%20size)](https://hub.docker.com/r/myanesp/comaps-server/)
[![License](https://badgen.net/github/license/myanesp/comaps-server)](LICENSE)
[![Project Status: Active](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Why?

Starting from CoMaps version [v2025.12.19-11](https://codeberg.org/comaps/comaps/releases/tag/v2025.12.19-11), you can set your own server for downloading map files, instead of using CoMaps CDN. This can be useful to reduce CDN loads or provide map files to your community.

## Features

- Download all map files for the whole world or only the ones you want
- Specify a whole country or only regions of it

## How to Run

### Run with Docker Compose

```yaml
services:
  maps-server:
    image: ghcr.io/myanesp/comaps-server
    container_name: comaps-server
    ports:
      - "80:80"
    environment:
      - MAPS=World,WorldCoasts,Spain
      - OUTPUT_DIR=/maps
    volumes:
      - ./maps:/maps
      - TZ=Europe/Madrid
```

### Run with Docker run

```yaml
docker run -d \
  --name comaps-server \
  --restart unless-stopped \
  -e MAPS=all \ 
  -e OUTPUT_DIR=/maps \
  -p "80:80" \
  ghcr.io/myanesp/comaps-server:latest
```

## Environment Variables

| VARIABLE | MANDATORY | DESCRIPTION | DEFAULT |
|----------|:---------:|-------------------------------------------------------------|---------|
| MAPS | ✅ | Map(s) to download. Can be "all", a country or a specific region | - |
| OUTPUT_DIR | ✅ | Directory to save all map files. /maps should be the choice in all cases | - |

## Planned features

- [ ] Autodownload maps when updates available
- [ ] Multiarch support