---
name: microservices-architecture
description: Master microservices architecture, service decomposition, and distributed systems patterns.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# Microservices Architecture

Scalable service-oriented design.

## Service Decomposition

- User Service
- Order Service
- Payment Service
- Inventory Service

## Communication

```
Service A ──REST──> Service B
Service A ──gRPC──> Service C
Service A ──Event──> Message Queue
```

## Patterns

- API Gateway
- Service Discovery
- Circuit Breaker
- Saga Pattern
- Event Sourcing

## Key Skills

- Service boundaries
- Data consistency
- Fault tolerance
- Monitoring
