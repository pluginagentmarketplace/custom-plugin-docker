# Docker Installation Guide

## Prerequisites

- 64-bit OS
- Linux kernel 3.10+ (for Linux)
- 4GB RAM minimum
- Virtualization enabled (for Windows/Mac)

## Post-Installation Steps

1. **Add user to docker group**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

2. **Configure Docker daemon**
   ```bash
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

3. **Verify installation**
   ```bash
   docker run hello-world
   ```

## Common Issues

### Permission denied
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

### Docker daemon not running
```bash
sudo systemctl start docker
```

## Docker Desktop vs Engine

| Feature | Desktop | Engine |
|---------|---------|--------|
| GUI | Yes | No |
| Kubernetes | Built-in | Manual |
| Platform | All | Linux only |
| License | Personal free | Free |
