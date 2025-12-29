---
name: docker-volumes
description: Master Docker volumes - data persistence, bind mounts, volume drivers, and backup strategies
sasmp_version: "1.3.0"
bonded_agent: docker-networking-storage
bond_type: PRIMARY_BOND
---

# Docker Volumes Skill

## Volume Types

### Named Volumes
```bash
docker volume create mydata
docker run -v mydata:/data myapp
```

### Bind Mounts
```bash
docker run -v $(pwd)/data:/data myapp
docker run -v /host/path:/container/path:ro myapp
```

### tmpfs Mounts
```bash
docker run --tmpfs /tmp myapp
```

## Volume Commands

```bash
docker volume ls
docker volume create mydata
docker volume inspect mydata
docker volume rm mydata
docker volume prune
```

## Backup & Restore

```bash
# Backup
docker run --rm -v mydata:/data -v $(pwd):/backup alpine \
  tar czf /backup/mydata.tar.gz /data

# Restore
docker run --rm -v mydata:/data -v $(pwd):/backup alpine \
  tar xzf /backup/mydata.tar.gz -C /
```

## Assets
- `backup-volume.sh` - Backup script

## References
- `VOLUME_GUIDE.md` - Best practices
