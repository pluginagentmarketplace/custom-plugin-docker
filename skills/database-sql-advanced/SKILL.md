---
name: database-sql-advanced
description: Advanced SQL and database optimization. Master query optimization, indexing, transactions, and building scalable data systems.
---

# Database & SQL Advanced

Optimize data storage and retrieval.

## Query Optimization

```sql
-- Index usage
CREATE INDEX idx_users_email ON users(email);
SELECT * FROM users WHERE email = 'user@example.com';

-- Explain query plan
EXPLAIN SELECT * FROM orders WHERE user_id = 1 AND created_at > '2024-01-01';

-- Window functions
SELECT user_id, amount,
       SUM(amount) OVER (PARTITION BY user_id) as total
FROM transactions;

-- Common table expressions
WITH user_totals AS (
  SELECT user_id, SUM(amount) as total FROM transactions GROUP BY user_id
)
SELECT u.*, ut.total FROM users u JOIN user_totals ut ON u.id = ut.user_id;
```

## Transaction Management

```sql
BEGIN TRANSACTION;

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

COMMIT; -- or ROLLBACK on error
```

## Database Design

- Normalization (1NF, 2NF, 3NF)
- Primary keys and foreign keys
- Index strategies
- Partitioning for scale
- Replication and failover
- Connection pooling

## ORMs

```typescript
// TypeORM
const user = await userRepository.findOne({ where: { id: 1 } });

// Prisma
const user = await prisma.user.findUnique({ where: { id: 1 } });

// SQLAlchemy (Python)
user = session.query(User).filter_by(id=1).first()
```

## Best Practices

1. Proper indexing strategy
2. Query optimization
3. Connection pooling
4. Transaction management
5. Data backup and recovery
6. Monitoring and alerting
7. Normalization vs denormalization
8. Replication for redundancy
