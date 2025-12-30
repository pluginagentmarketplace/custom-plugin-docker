# Docker Registry Guide

## Quick Start

### Run Local Registry
```bash
docker run -d -p 5000:5000 --name registry registry:2
```

### Push Image to Registry
```bash
# Tag the image
docker tag myapp:latest localhost:5000/myapp:latest

# Push to registry
docker push localhost:5000/myapp:latest
```

### Pull Image from Registry
```bash
docker pull localhost:5000/myapp:latest
```

## Authentication Setup

### Create Password File
```bash
mkdir auth
docker run --rm --entrypoint htpasswd \
  httpd:2 -Bbn admin password123 > auth/htpasswd
```

### Run with Authentication
```bash
docker run -d -p 5000:5000 \
  -v $(pwd)/auth:/auth \
  -e "REGISTRY_AUTH=htpasswd" \
  -e "REGISTRY_AUTH_HTPASSWD_REALM=Registry" \
  -e "REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd" \
  --name registry registry:2
```

### Login to Registry
```bash
docker login localhost:5000
```

## TLS Configuration

### Generate Self-Signed Certificate
```bash
mkdir certs
openssl req -newkey rsa:4096 -nodes -sha256 \
  -keyout certs/domain.key -x509 -days 365 \
  -out certs/domain.crt
```

### Run with TLS
```bash
docker run -d -p 443:443 \
  -v $(pwd)/certs:/certs \
  -e REGISTRY_HTTP_ADDR=0.0.0.0:443 \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  --name registry registry:2
```

## Registry API

### List Repositories
```bash
curl http://localhost:5000/v2/_catalog
```

### List Tags
```bash
curl http://localhost:5000/v2/myapp/tags/list
```

### Delete Image
```bash
# Get digest
DIGEST=$(curl -I -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  http://localhost:5000/v2/myapp/manifests/latest 2>&1 | \
  grep Docker-Content-Digest | awk '{print $2}' | tr -d '\r')

# Delete
curl -X DELETE http://localhost:5000/v2/myapp/manifests/$DIGEST
```

## Garbage Collection

```bash
# Run garbage collection
docker exec registry bin/registry garbage-collect \
  /etc/docker/registry/config.yml

# Dry run first
docker exec registry bin/registry garbage-collect \
  --dry-run /etc/docker/registry/config.yml
```
