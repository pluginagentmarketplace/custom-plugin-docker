#!/bin/bash
# Common Docker Run Patterns

# Web server with port mapping
docker run -d --name nginx-web \
  -p 80:80 \
  -v $(pwd)/html:/usr/share/nginx/html:ro \
  nginx:alpine

# Database with persistence
docker run -d --name postgres-db \
  -e POSTGRES_PASSWORD=secret \
  -e POSTGRES_DB=myapp \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15-alpine

# Redis cache
docker run -d --name redis-cache \
  -p 6379:6379 \
  redis:7-alpine

# Application with limits
docker run -d --name myapp \
  --memory=256m \
  --cpus=0.5 \
  --restart=unless-stopped \
  -e NODE_ENV=production \
  -p 3000:3000 \
  myapp:latest
