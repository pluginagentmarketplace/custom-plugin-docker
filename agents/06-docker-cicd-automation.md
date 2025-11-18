---
description: Master Docker in CI/CD pipelines. Learn automated builds, testing in containers, deployment strategies, and container-native DevOps practices.
capabilities: ["GitHub Actions", "Docker build automation", "Container testing", "Registry integration", "Multi-stage pipelines", "Deployment automation", "Blue-green deployments", "Rollback strategies", "Monitoring integration"]
---

# 🐳 Docker CI/CD & Automation

## Overview
Automated Docker builds and deployments with CI/CD pipelines.

## GitHub Actions Workflow

```yaml
name: Docker Build & Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: |
          username/myapp:latest
          username/myapp:${{ github.sha }}

    - name: Run tests
      run: docker run --rm username/myapp:${{ github.sha }} npm test

    - name: Scan image
      run: docker scan username/myapp:${{ github.sha }}
```

## Multi-Stage Pipeline

```yaml
name: Full CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Run tests in container
      run: |
        docker build --target test -t myapp:test .
        docker run --rm myapp:test npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Build production image
      run: docker build -t myapp:${{ github.sha }} .

    - name: Push to registry
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker tag myapp:${{ github.sha }} username/myapp:latest
        docker push username/myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - name: Deploy to production
      run: |
        ssh deploy@server "docker pull username/myapp:latest && docker compose -f /app/docker-compose.yml up -d"
```

## Docker in Jenkins

```groovy
pipeline {
    agent any

    environment {
        REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myapp'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    sh 'docker build -t ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} .'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'docker run --rm ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER} npm test'
                }
            }
        }

        stage('Push') {
            steps {
                script {
                    sh '''
                        docker login -u ${DOCKER_USER} -p ${DOCKER_PASS} ${REGISTRY}
                        docker push ${REGISTRY}/${IMAGE_NAME}:${BUILD_NUMBER}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'ssh -i deploy.key deploy@prod docker pull ${REGISTRY}/${IMAGE_NAME}:latest'
                }
            }
        }
    }
}
```

## Dockerfile for Testing

```dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS dependencies
RUN npm ci

FROM base AS test
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
RUN npm test

FROM base AS production
COPY --from=dependencies /app/node_modules ./node_modules
COPY src ./src
EXPOSE 3000
CMD ["node", "src/index.js"]
```

## Blue-Green Deployment

```yaml
# blue-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-blue
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: blue

---
# green-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-green
spec:
  replicas: 3
  selector:
    matchLabels:
      app: myapp
      version: green

---
# Service points to blue (current)
apiVersion: v1
kind: Service
metadata:
  name: myapp
spec:
  selector:
    app: myapp
    version: blue  # Switch to green after validation
  ports:
  - port: 80
    targetPort: 3000
```

## Container Image Scanning

```bash
# Trivy scanning
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image myapp:latest

# Docker Scout
docker scout cves myapp:latest

# Vulnerability reporting
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  anchore/grype:latest myapp:latest
```

## Learning Path

### Beginner (15 hours)
1. GitHub Actions basics
2. Docker build automation
3. Image registry integration
4. Basic testing in containers
5. Simple deployment

### Intermediate (20 hours)
1. Multi-stage pipelines
2. Advanced testing strategies
3. Image scanning
4. Rolling deployments
5. Monitoring integration

### Advanced (15 hours)
1. Blue-green deployments
2. Canary releases
3. GitOps workflows
4. Advanced Kubernetes deployments
5. Automated rollback

## Best Practices

1. **Automated testing** (before deployment)
2. **Image scanning** (security first)
3. **Version tagging** (reproducibility)
4. **Progressive deployment** (minimize risk)
5. **Rollback capability** (always)
6. **Deployment automation** (no manual steps)
7. **Environment separation** (dev, test, prod)
8. **CI/CD monitoring** (track all deployments)
