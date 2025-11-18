---
name: docker-kubernetes
description: Master Docker containers in Kubernetes. Learn Deployments, Services, ConfigMaps, Secrets, and Persistent Volumes for production container orchestration. Use when running Docker containers on Kubernetes.
---

# Docker in Kubernetes

Run Docker containers at scale on Kubernetes.

## Basic Deployment

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
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:1.0
        ports:
        - containerPort: 3000
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
```

## Service Exposure

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  type: LoadBalancer
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
```

## ConfigMap & Secrets

```yaml
# ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: production

# Secret
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
data:
  password: c2VjcmV0  # base64 encoded
```

## kubectl Commands

```bash
# Apply manifests
kubectl apply -f deployment.yaml

# Inspect
kubectl get pods
kubectl logs myapp-xyz
kubectl exec -it myapp-xyz -- bash

# Update
kubectl set image deployment/myapp app=myapp:2.0
kubectl rollout history deployment/myapp
kubectl rollout undo deployment/myapp
```

## Key Concepts

- Deployments
- Pods
- Services
- ConfigMaps
- Secrets
- Persistent Volumes
- Scaling
- Rolling updates
- Health checks

## Best Practices

1. Use Deployments (not bare Pods)
2. Define resource limits
3. Health checks (liveness/readiness)
4. Gradual rollouts
5. ConfigMaps for config
6. Secrets for sensitive data
7. Persistent volumes for data
8. Service discovery via DNS
