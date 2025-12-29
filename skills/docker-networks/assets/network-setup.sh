#!/bin/bash
# Docker Network Setup Script

# Create isolated networks
docker network create --driver bridge frontend-net
docker network create --driver bridge backend-net

# Database on backend only
docker run -d --name db --network backend-net postgres:15-alpine

# API on both networks
docker run -d --name api --network backend-net myapi
docker network connect frontend-net api

# Web on frontend only
docker run -d --name web --network frontend-net -p 80:80 nginx
