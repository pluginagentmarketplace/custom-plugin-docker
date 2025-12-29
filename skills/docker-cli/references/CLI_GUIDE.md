# Docker CLI Reference

## Format Output

```bash
docker ps --format "{{.Names}}: {{.Status}}"
docker images --format "{{.Repository}}:{{.Tag}} {{.Size}}"
```

## Filter

```bash
docker ps -f status=exited
docker images -f dangling=true
```

## Cleanup

```bash
docker system prune       # Unused data
docker system prune -a    # All unused
docker volume prune       # Unused volumes
docker network prune      # Unused networks
```
