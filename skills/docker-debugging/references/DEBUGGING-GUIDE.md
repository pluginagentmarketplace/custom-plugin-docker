# Docker Debugging Guide

## Quick Reference

### Container Won't Start

1. **Check exit code:**
   ```bash
   docker inspect -f '{{.State.ExitCode}}' <container>
   ```
   - Exit 0: Normal termination
   - Exit 1: Application error
   - Exit 137: OOM killed (out of memory)
   - Exit 139: Segmentation fault
   - Exit 143: SIGTERM received

2. **View logs:**
   ```bash
   docker logs <container>
   ```

3. **Debug entrypoint:**
   ```bash
   docker run -it --entrypoint /bin/sh <image>
   ```

### High Memory Usage

1. **Check current usage:**
   ```bash
   docker stats <container>
   ```

2. **Set memory limits:**
   ```bash
   docker run -m 512m --memory-swap 1g <image>
   ```

3. **Find memory hogs:**
   ```bash
   docker exec <container> ps aux --sort=-%mem | head
   ```

### Network Issues

1. **Container can't reach internet:**
   ```bash
   # Check DNS
   docker exec <container> cat /etc/resolv.conf

   # Test connectivity
   docker exec <container> ping -c 3 8.8.8.8
   ```

2. **Containers can't communicate:**
   ```bash
   # Ensure same network
   docker network inspect <network>

   # Use container name as hostname
   docker exec <container1> ping <container2_name>
   ```

### Disk Space Issues

1. **Check Docker disk usage:**
   ```bash
   docker system df -v
   ```

2. **Cleanup unused resources:**
   ```bash
   # Remove unused containers, networks, images
   docker system prune -a

   # Remove unused volumes
   docker volume prune
   ```

## Best Practices

1. **Always use health checks** in Dockerfiles
2. **Set resource limits** to prevent runaway containers
3. **Use logging drivers** for centralized log management
4. **Tag images properly** for easier debugging
5. **Keep containers stateless** - data in volumes
