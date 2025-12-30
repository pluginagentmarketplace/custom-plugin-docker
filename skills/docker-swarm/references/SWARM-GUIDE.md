# Docker Swarm Guide

## Quick Start

### Initialize Swarm
```bash
docker swarm init --advertise-addr <MANAGER-IP>
```

### Join Nodes
```bash
# Get worker token
docker swarm join-token worker

# Get manager token
docker swarm join-token manager
```

### Deploy Stack
```bash
docker stack deploy -c docker-compose.yml myapp
```

## Service Management

### Create Service
```bash
docker service create --name web --replicas 3 -p 80:80 nginx
```

### Scale Service
```bash
docker service scale web=5
```

### Update Service
```bash
docker service update --image nginx:latest web
```

### Rollback
```bash
docker service rollback web
```

## Monitoring

### View Services
```bash
docker service ls
```

### View Tasks
```bash
docker service ps web
```

### View Logs
```bash
docker service logs -f web
```

## Secrets Management

### Create Secret
```bash
echo "mypassword" | docker secret create db_password -
```

### Use in Service
```bash
docker service create --secret db_password myapp
```

## Best Practices

1. **Use 3+ managers** for high availability
2. **Drain nodes** before maintenance
3. **Use placement constraints** for data services
4. **Set resource limits** on all services
5. **Use health checks** for automatic recovery
6. **Overlay networks** for service isolation

## Common Commands

| Command | Description |
|---------|-------------|
| `docker node ls` | List nodes |
| `docker service ls` | List services |
| `docker stack ls` | List stacks |
| `docker node update --availability drain NODE` | Drain node |
| `docker swarm leave --force` | Leave swarm |
