---
name: backend-development
description: Build scalable backend systems with Node.js, Python, Java, Go, and Rust. Learn API design, database optimization, authentication, microservices, and production-ready deployment. Use when working on server-side development.
---

# Backend Development

Design and implement robust, scalable server-side systems.

## Quick Start

### Node.js with Express & TypeScript
```typescript
import express, { Express, Request, Response } from 'express';

const app: Express = express();
app.use(express.json());

interface User {
  id: string;
  name: string;
  email: string;
}

// GET endpoint
app.get('/users/:id', async (req: Request, res: Response) => {
  try {
    const user: User = await fetchUser(req.params.id);
    res.json(user);
  } catch (error) {
    res.status(500).json({ error: 'User not found' });
  }
});

// POST endpoint
app.post('/users', async (req: Request, res: Response) => {
  const newUser: User = req.body;
  const created = await createUser(newUser);
  res.status(201).json(created);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Python with FastAPI
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class User(BaseModel):
    id: str
    name: str
    email: str

@app.get("/users/{user_id}")
async def get_user(user_id: str) -> User:
    user = await fetch_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users")
async def create_user(user: User) -> User:
    created = await save_user(user)
    return created
```

### Database Query (PostgreSQL)
```typescript
// Using TypeORM
import { createConnection, Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  name: string;

  @Column({ unique: true })
  email: string;
}

// Query
const userRepository = connection.getRepository(User);
const users = await userRepository.find({
  where: { email: 'user@example.com' }
});
```

## Key Concepts

### API Design
- RESTful principles (HTTP methods, status codes)
- Versioning strategies (URL, header, query)
- Pagination and filtering
- Error handling and response formats

### Database Design
- Normalization and schema design
- Indexing strategies
- Query optimization
- Transaction management

### Authentication & Security
- JWT token handling
- OAuth2 implementation
- Password hashing (bcrypt, Argon2)
- Rate limiting and throttling

### Scalability Patterns
- Caching (Redis, Memcached)
- Database replication and sharding
- Load balancing
- Message queues for async processing

## Common Patterns

### Repository Pattern
```typescript
interface IUserRepository {
  findById(id: string): Promise<User>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<void>;
}

class UserRepository implements IUserRepository {
  async findById(id: string): Promise<User> {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
}
```

### Dependency Injection
```typescript
class UserService {
  constructor(
    private userRepository: IUserRepository,
    private emailService: IEmailService
  ) {}

  async createUser(userData: UserData): Promise<User> {
    const user = await this.userRepository.save(userData);
    await this.emailService.sendWelcome(user.email);
    return user;
  }
}
```

### Async Request Handling
```typescript
app.post('/heavy-operation', async (req, res) => {
  const jobId = generateId();

  // Queue the operation
  queue.enqueue({
    id: jobId,
    operation: 'process-data',
    data: req.body
  });

  // Return immediately with job ID
  res.accepted({ jobId, statusUrl: `/jobs/${jobId}` });
});
```

## Best Practices

1. **Use async/await** - Handle concurrency properly
2. **Implement proper error handling** - Use try-catch, error middleware
3. **Validate all inputs** - Prevent injection attacks
4. **Use prepared statements** - Prevent SQL injection
5. **Implement logging** - Structured logging for debugging
6. **Rate limiting** - Protect against abuse
7. **API versioning** - Support multiple versions gracefully
8. **Health checks** - Implement /health endpoints

## Tools & Libraries

**Authentication**: jsonwebtoken, passport, oauth2orize
**Validation**: Joi, Yup, class-validator
**ORM**: Sequelize, TypeORM, Prisma, SQLAlchemy
**HTTP Client**: Axios, node-fetch, requests
**Testing**: Jest, Mocha, pytest
**Database**: PostgreSQL, MongoDB, Redis
