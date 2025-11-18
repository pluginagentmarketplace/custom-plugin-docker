---
name: system-design
description: Master system design and architecture patterns. Learn scalability, reliability, distributed systems, microservices, and real-world system design. Use when designing large systems or making architectural decisions.
---

# System Design

Design scalable, reliable systems from the ground up.

## Quick Start

### Horizontal Scaling with Load Balancer
```
┌─────────────────────────────────────────┐
│         Client Requests                 │
└──────────────┬──────────────────────────┘
               │
               ▼
        ┌─────────────┐
        │Load Balancer│
        └─────┬───────┘
              │
      ┌───────┼───────┬──────────┐
      ▼       ▼       ▼          ▼
    [WEB1] [WEB2] [WEB3]    [WEB4]
      │       │       │          │
      └───────┼───────┴──────────┘
              │
              ▼
        ┌──────────────┐
        │   Database   │
        └──────────────┘
```

### Database Replication
```sql
-- Master-Slave Setup
-- Master: Writes go here
INSERT INTO users (name) VALUES ('John');

-- Slaves: Replicate data asynchronously
SELECT * FROM users; -- Read from slave
```

### Caching Strategy
```python
class CacheLayer:
    def __init__(self):
        self.redis = Redis()

    def get_user(self, user_id):
        # Try cache first
        cached = self.redis.get(f"user:{user_id}")
        if cached:
            return json.loads(cached)

        # Cache miss - fetch from DB
        user = self.db.query(User).get(user_id)

        # Store in cache (1 hour TTL)
        self.redis.setex(
            f"user:{user_id}",
            3600,
            json.dumps(user)
        )
        return user

    def invalidate_user(self, user_id):
        self.redis.delete(f"user:{user_id}")
```

### Message Queue Pattern
```python
# Producer
def create_order(order_data):
    order = save_to_db(order_data)

    # Publish event
    message_queue.publish('order.created', {
        'order_id': order.id,
        'user_id': order.user_id,
        'amount': order.amount
    })

    return order

# Consumer
def process_order(message):
    order_id = message['order_id']

    # Charge payment
    payment_result = payment_service.charge(
        message['user_id'],
        message['amount']
    )

    if payment_result.success:
        send_confirmation_email(message['user_id'])
    else:
        publish_event('order.failed', message)
```

### Circuit Breaker Pattern
```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise

    def on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'

    def on_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

# Usage
breaker = CircuitBreaker()
try:
    breaker.call(external_api.call)
except Exception:
    # Fallback
    return cached_result
```

## Key Concepts

### Scalability
- **Horizontal**: Add more servers
- **Vertical**: Stronger server
- **Database**: Sharding, replication, read replicas
- **Caching**: Redis, Memcached at multiple levels

### Reliability
- **Redundancy**: Eliminate single points of failure
- **Failover**: Automatic recovery
- **Health checks**: Monitor component health
- **Graceful degradation**: Continue with reduced functionality

### Consistency
- **Strong consistency**: ACID transactions
- **Eventual consistency**: Accepting temporary inconsistency
- **CAP theorem**: Choose two of Consistency, Availability, Partition tolerance

### Performance
- **Latency**: Response time
- **Throughput**: Requests per second
- **Bottlenecks**: Find and eliminate
- **CDN**: Cache content geographically

## Common Architectures

### Microservices
```
User Service  Order Service  Payment Service
     ↓              ↓              ↓
[API Gateway]
     ↓
  Message Queue (Kafka)
     ↓
[Service Mesh - Istio]
```

### Event-Driven
```
User Signs Up → Event Bus → Email Service
                         → Analytics Service
                         → Notification Service
```

### CQRS (Command Query Responsibility Segregation)
```
Commands (Write)          Queries (Read)
    ↓                          ↓
  Database ←────────────── Event Store
                ↓
          Read Model Cache
```

## Best Practices

1. **Start simple** - Don't over-engineer initially
2. **Identify bottlenecks** - Profile before optimizing
3. **Design for failure** - Assume parts will fail
4. **Monitor everything** - Can't optimize what you can't measure
5. **Cache wisely** - Understand cache invalidation
6. **Use appropriate databases** - SQL vs. NoSQL tradeoffs
7. **Plan for growth** - Anticipate scaling needs
8. **Document decisions** - Capture architecture decisions

## Tools & Technologies

**Load Balancing**: Nginx, HAProxy, AWS ELB
**Caching**: Redis, Memcached, Varnish
**Message Queues**: RabbitMQ, Kafka, AWS SQS
**Databases**: PostgreSQL, MongoDB, DynamoDB
**Monitoring**: Prometheus, Grafana, Datadog
**Service Mesh**: Istio, Linkerd
