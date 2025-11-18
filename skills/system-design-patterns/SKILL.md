---
name: system-design-patterns
description: Master system design fundamentals, scalability patterns, and designing large-scale applications.
---

# System Design Patterns

Scalable system architecture.

## Design Patterns

- Singleton, Factory, Builder
- Observer, Strategy, Decorator
- Adapter, Bridge, Proxy

## Scalability

```
Load Balancer
    ↓
[Web1] [Web2] [Web3]
    ↓
Cache (Redis)
    ↓
Database + Replicas
```

## Key Concepts

- Horizontal vs vertical scaling
- Caching strategies
- Database replication
- Message queues
- API design
