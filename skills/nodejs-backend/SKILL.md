---
name: nodejs-backend
description: Master Node.js backend development with Express, Fastify, async/await, and building production APIs. Learn best practices for server-side JavaScript.
---

# Node.js Backend

Production-ready Node.js development.

## Express Server

```typescript
import express from 'express'
import { json } from 'body-parser'

const app = express()
app.use(json())

// Middleware
app.use((req, res, next) => {
  console.log(req.method, req.url)
  next()
})

// Routes
app.get('/api/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id)
  res.json(user)
})

app.post('/api/users', async (req, res) => {
  const user = await db.users.create(req.body)
  res.status(201).json(user)
})

// Error handling
app.use((err, req, res, next) => {
  console.error(err)
  res.status(500).json({ error: 'Internal error' })
})

app.listen(3000)
```

## Async/Await Patterns

```typescript
// Promise chain vs async/await
// Old way
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(r => r.json())
    .then(user => fetchPosts(user.id))
}

// Modern way
async function fetchUser(id) {
  const user = await fetch(`/api/users/${id}`).then(r => r.json())
  const posts = await fetchPosts(user.id)
  return { user, posts }
}

// Error handling
try {
  const data = await fetchData()
} catch (error) {
  console.error('Failed:', error.message)
}

// Parallel execution
const [users, posts] = await Promise.all([
  fetchUsers(),
  fetchPosts()
])
```

## Fastify Performance

```typescript
import Fastify from 'fastify'

const fastify = Fastify()

fastify.get('/api/users/:id', async (request, reply) => {
  const user = await db.users.findById(request.params.id)
  return user
})

fastify.listen({ port: 3000 })
```

## Key Concepts

- Event-driven architecture
- Stream processing
- Middleware patterns
- Error handling
- Async operations
- Performance optimization
- Testing strategies

## Best Practices

1. Use async/await
2. Proper error handling
3. Input validation
4. Rate limiting
5. Security headers
6. Logging strategy
7. Database connection pooling
8. Graceful shutdown
