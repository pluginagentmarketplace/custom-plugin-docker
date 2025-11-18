---
name: docker-kubernetes-terraform
description: Master Docker containerization, Kubernetes orchestration, and Terraform infrastructure as code for scalable production systems.
---

# Docker, Kubernetes & Terraform

Container and infrastructure management.

## Docker

```bash
docker build -t app:1.0 .
docker run -d -p 8080:3000 app:1.0
docker compose up -d
```

## Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
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
        image: app:1.0
        ports:
        - containerPort: 3000
```

## Terraform

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  tags = { Name = "web-server" }
}
```

## Key Skills

- Container optimization
- Cluster management
- Infrastructure automation
- Cloud deployment
- Monitoring setup
