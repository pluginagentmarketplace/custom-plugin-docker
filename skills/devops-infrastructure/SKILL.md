---
name: devops-infrastructure
description: Master Docker, Kubernetes, AWS, Terraform, and CI/CD pipelines. Learn containerization, orchestration, infrastructure-as-code, and cloud deployment strategies. Use when working on DevOps or infrastructure tasks.
---

# DevOps & Infrastructure

Build reliable, scalable infrastructure and deployment pipelines.

## Quick Start

### Docker Dockerfile
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy app
COPY . .

# Build if needed
RUN npm run build

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD node healthcheck.js

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgres://db:5432/myapp
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
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

### Terraform AWS
```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

# EC2 Instance
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"

  tags = {
    Name = "web-server"
  }
}

# RDS Database
resource "aws_db_instance" "postgres" {
  identifier     = "mydb"
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.t3.micro"
}
```

### CI/CD Pipeline (GitHub Actions)
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm install
      - run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          kubectl set image deployment/app-deployment \
            app=myapp:${{ github.sha }}
```

## Key Concepts

### Containerization
- Image optimization (multi-stage builds, minimal base images)
- Container best practices (one process per container)
- Volume and networking
- Registry management (Docker Hub, ECR, GCR)

### Orchestration
- Pod scheduling and node management
- Service discovery and load balancing
- ConfigMaps and Secrets
- Persistent volumes and storage classes

### Infrastructure as Code
- Declarative vs. imperative
- State management in Terraform
- Modules and reusability
- Secrets handling

### CI/CD
- Build, test, deploy stages
- Artifact management
- Environment promotion
- Rollback strategies

## Common Patterns

### Blue-Green Deployment
```bash
# Deploy new version to "green" environment
kubectl apply -f deployment-green.yaml

# Test green environment
curl https://green.example.com/health

# Switch traffic
kubectl patch service myapp -p \
  '{"spec":{"selector":{"version":"green"}}}'

# Keep blue running for rollback
```

### Canary Deployment
```yaml
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: myapp
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  service:
    port: 3000
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
```

## Best Practices

1. **Immutable infrastructure** - Rebuild rather than modify
2. **Infrastructure as Code** - Version control all infrastructure
3. **Secrets management** - Use vaults, never hardcode
4. **Monitoring and logging** - Observability from day one
5. **Automated testing** - Test infrastructure changes
6. **Rollback strategy** - Always have a rollback plan
7. **Resource limits** - Set requests and limits for containers
8. **Security scanning** - Scan images and dependencies

## Tools & Technologies

**Containerization**: Docker, Podman
**Orchestration**: Kubernetes, Docker Swarm, OpenShift
**Cloud**: AWS, Azure, Google Cloud, DigitalOcean
**IaC**: Terraform, CloudFormation, Pulumi, Ansible
**CI/CD**: GitHub Actions, GitLab CI, Jenkins, CircleCI
**Monitoring**: Prometheus, Grafana, ELK, Datadog
