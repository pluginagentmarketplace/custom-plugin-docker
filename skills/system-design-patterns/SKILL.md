---
name: system-design-patterns
description: Master system design fundamentals, scalability patterns, and designing large-scale applications.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
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
