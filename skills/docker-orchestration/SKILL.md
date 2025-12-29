---
name: docker-orchestration
description: Docker orchestration - Swarm, Kubernetes basics, scaling, and production deployment
sasmp_version: "1.3.0"
bonded_agent: docker-production
bond_type: PRIMARY_BOND
---

# Docker Orchestration Skill

## Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml myapp

# Scale service
docker service scale myapp_web=3

# List services
docker service ls
docker service ps myapp_web
```

## Kubernetes Basics

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
        - name: myapp
          image: myapp:v1
          ports:
            - containerPort: 3000
```

## Scaling Strategies

| Platform | Command |
|----------|---------|
| Swarm | docker service scale |
| K8s | kubectl scale |
| Compose | docker compose up --scale |

## Assets
- `swarm-stack.yml` - Swarm deployment

## References
- `ORCHESTRATION_GUIDE.md` - Comparison
