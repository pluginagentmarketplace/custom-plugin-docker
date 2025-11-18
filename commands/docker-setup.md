# /docker-setup - Docker Installation & Setup Guide

Complete Docker environment setup and verification.

## Description

Get a detailed setup guide for Docker on your system, including installation, configuration, and verification.

## Setup Steps

### Installation

**macOS:**
```bash
brew install docker
```

**Ubuntu:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Windows:**
- Download Docker Desktop
- Follow installer
- Enable WSL 2 backend

### Verification

```bash
docker --version
docker run hello-world
```

### Configuration

```bash
# Create daemon config
cat > ~/.docker/config.json << 'EOF'
{
  "experimental": true,
  "buildkit": true
}
EOF

# Enable BuildKit
export DOCKER_BUILDKIT=1
```

## Common Issues

1. **Permission denied** - Add user to docker group
2. **Docker daemon not running** - Start Docker service
3. **Port already in use** - Change port mapping
4. **Out of disk space** - Run `docker system prune`

## Verify Installation

- ✅ Docker CLI working
- ✅ Docker daemon running
- ✅ Can pull images
- ✅ Can run containers
- ✅ Can build images

## Next Steps

- Learn Docker Fundamentals
- Build your first Dockerfile
- Run Docker Compose
- Deploy to production
