# /docker-deploy-monitor - Docker Deployment & Monitoring

Production deployment and monitoring commands.

## Description

Deploy Docker containers to production and monitor their health and performance.

## Registry Operations

```bash
# Login to registry
docker login registry.example.com

# Tag image
docker tag myapp:1.0 registry.example.com/myapp:1.0

# Push image
docker push registry.example.com/myapp:1.0

# Pull image
docker pull registry.example.com/myapp:1.0

# Logout
docker logout registry.example.com
```

## Kubernetes Deployment

```bash
# Apply manifest
kubectl apply -f deployment.yaml

# Check status
kubectl get deployments
kubectl get pods

# View logs
kubectl logs pod-name
kubectl logs -f deployment/myapp

# Scale deployment
kubectl scale deployment myapp --replicas=5

# Update image
kubectl set image deployment/myapp app=registry.io/myapp:2.0

# Rolling update status
kubectl rollout status deployment/myapp

# Rollback
kubectl rollout undo deployment/myapp
```

## Monitoring & Debugging

```bash
# Container stats
docker stats

# View logs
docker logs container-id
docker logs -f container-id
docker logs --tail 100 container-id

# Inspect container
docker inspect container-id

# Check processes
docker top container-id

# Event monitoring
docker events

# Check resources
docker system df
docker system prune

# Health check
docker ps --format "table {{.Names}}\t{{.Status}}"
```

## Production Checklist

```markdown
## Pre-Deployment
- [ ] Image built and tagged
- [ ] Image scanned for vulnerabilities
- [ ] All tests passing
- [ ] Database migrations ready
- [ ] Environment variables set
- [ ] Secrets configured
- [ ] Health checks defined
- [ ] Resource limits set

## Deployment
- [ ] Rollback plan ready
- [ ] Monitoring alerts configured
- [ ] Logging enabled
- [ ] Backup strategy ready
- [ ] DNS configured
- [ ] SSL/TLS enabled
- [ ] Load balancer configured
- [ ] Network policies applied

## Post-Deployment
- [ ] Verify all services running
- [ ] Check health endpoints
- [ ] Monitor logs for errors
- [ ] Test critical features
- [ ] Verify backups working
- [ ] Check monitoring dashboards
- [ ] Performance metrics normal
- [ ] No alert triggers
```

## Useful Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias dk='docker'
alias dkps='docker ps'
alias dklog='docker logs -f'
alias dkexec='docker exec -it'
alias dkcomposeup='docker compose up -d'
alias dkcomposedown='docker compose down'
alias dkstats='docker stats'
```

## Backup & Restore

```bash
# Backup volume
docker run --rm -v myvolume:/data -v $(pwd):/backup \
  alpine tar czf /backup/backup.tar.gz /data

# Restore volume
docker run --rm -v myvolume:/data -v $(pwd):/backup \
  alpine tar xzf /backup/backup.tar.gz -C /

# Backup database
docker exec mydb pg_dump -U user dbname | gzip > backup.sql.gz

# Restore database
gunzip -c backup.sql.gz | docker exec -i mydb psql -U user dbname
```

## Emergency Recovery

```bash
# Restart all containers
docker restart $(docker ps -aq)

# Remove failed containers
docker rm $(docker ps -q --filter "status=exited")

# Clean unused resources
docker system prune -a --volumes

# Reset Docker
docker system prune -a --volumes
# WARNING: Removes all unused data

# Check disk usage
docker system df
```

## Monitoring Tools

```bash
# Prometheus export
docker run -d --name prometheus prom/prometheus

# Grafana dashboard
docker run -d --name grafana grafana/grafana

# ELK Stack
docker run -d --name elasticsearch docker.elastic.co/elasticsearch/elasticsearch:8.0.0
docker run -d --name kibana docker.elastic.co/kibana/kibana:8.0.0

# Portainer management
docker run -d --name portainer -p 9000:9000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  portainer/portainer-ce
```
