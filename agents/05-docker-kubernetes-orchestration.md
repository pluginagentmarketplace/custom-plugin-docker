---
description: Master container orchestration with Kubernetes. Learn deployments, services, volumes, ConfigMaps, and managing containerized applications at scale.
capabilities: ["Kubernetes basics", "Deployments", "Services", "ConfigMaps & Secrets", "Persistent volumes", "Pod management", "Scaling", "Health checks", "Rolling updates"]
---

# 🐳 Docker & Kubernetes Orchestration

## Overview
Running Docker containers at scale with Kubernetes.

## Basic Kubernetes Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    ports:
    - containerPort: 3000
    env:
    - name: NODE_ENV
      value: "production"
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    livenessProbe:
      httpGet:
        path: /health
        port: 3000
      initialDelaySeconds: 10
      periodSeconds: 10
```

## Deployment with Rolling Updates

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-deployment
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
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
          initialDelaySeconds: 15
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
```

## Service Exposure

```yaml
# ClusterIP - Internal only
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  type: ClusterIP
  selector:
    app: myapp
  ports:
  - port: 3000
    targetPort: 3000

---
# LoadBalancer - External access
apiVersion: v1
kind: Service
metadata:
  name: myapp-lb
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
# ConfigMap - Non-sensitive config
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  DATABASE_HOST: "postgres.default.svc.cluster.local"

---
# Secret - Sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: c2VjdXJlMTIz  # base64 encoded
  API_KEY: YWJjMTIz

---
# Pod using both
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
  - name: app
    image: myapp:1.0
    envFrom:
    - configMapRef:
        name: app-config
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: app-secrets
          key: DATABASE_PASSWORD
    volumeMounts:
    - name: config
      mountPath: /etc/config
      readOnly: true
  volumes:
  - name: config
    configMap:
      name: app-config
```

## Persistent Volumes

```yaml
# PersistentVolume
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-postgres
spec:
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /data/postgres

---
# PersistentVolumeClaim
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi

---
# Pod using PVC
apiVersion: v1
kind: Pod
metadata:
  name: postgres
spec:
  containers:
  - name: db
    image: postgres:15
    volumeMounts:
    - name: data
      mountPath: /var/lib/postgresql/data
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: postgres-pvc
```

## Essential kubectl Commands

```bash
# Deployment
kubectl apply -f deployment.yaml
kubectl get deployments
kubectl describe deployment myapp-deployment
kubectl set image deployment/myapp-deployment app=myapp:2.0

# Pods
kubectl get pods
kubectl logs myapp-pod
kubectl exec -it myapp-pod -- /bin/bash
kubectl port-forward myapp-pod 3000:3000

# Services
kubectl get services
kubectl expose deployment myapp --type=LoadBalancer
kubectl get endpoints

# ConfigMaps & Secrets
kubectl create configmap app-config --from-literal=KEY=value
kubectl create secret generic db-password --from-literal=password=secret
```

## Learning Path

### Beginner (20 hours)
1. Kubernetes basics
2. Pods and containers
3. Deployments
4. Services
5. ConfigMaps

### Intermediate (25 hours)
1. Persistent volumes
2. Health checks
3. Rolling updates
4. Scaling
5. Resource management

### Advanced (20 hours)
1. StatefulSets
2. DaemonSets
3. Ingress
4. Network policies
5. RBAC

## Best Practices

1. **Use Deployments** (not bare Pods)
2. **Define resource limits** (CPU, memory)
3. **Health checks** (liveness and readiness)
4. **Gradual rollouts** (rolling updates)
5. **ConfigMaps for configuration** (not hardcoded)
6. **Secrets for sensitive data** (encrypted)
7. **PersistentVolumes for data** (stateful)
8. **Pod disruption budgets** (availability)
