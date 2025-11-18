---
name: api-design-graphql
description: Master API design principles and GraphQL. Learn REST best practices, GraphQL schema design, resolvers, and building efficient APIs.
---

# API Design & GraphQL

Modern API architecture.

## REST Best Practices

```typescript
// Proper HTTP methods
GET    /api/users          // List
POST   /api/users          // Create
GET    /api/users/:id      // Detail
PUT    /api/users/:id      // Update
DELETE /api/users/:id      // Delete

// Status codes
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
500 Internal Server Error

// Resource design
/api/v1/users/:id/posts    // Nested resources
/api/v1/users?page=1&limit=10  // Pagination
```

## GraphQL Schema

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

type Query {
  user(id: ID!): User
  posts(limit: Int, offset: Int): [Post!]!
}

type Mutation {
  createUser(name: String!, email: String!): User!
  updateUser(id: ID!, name: String): User
}

type Subscription {
  userCreated: User!
}
```

## GraphQL Resolvers

```typescript
const resolvers = {
  Query: {
    user: (_, { id }) => db.users.findById(id),
    posts: (_, { limit, offset }) => db.posts.find({}, limit, offset),
  },
  Mutation: {
    createUser: (_, { name, email }) => db.users.create({ name, email }),
  },
  User: {
    posts: (user) => db.posts.find({ userId: user.id }),
  },
}
```

## API Versioning

```
/api/v1/users        // Version 1
/api/v2/users        // Version 2
Accept: application/vnd.api+json;version=2
X-API-Version: 2
```

## Performance

```typescript
// Caching
app.get('/api/users', cache('5 minutes'), handler)

// Rate limiting
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }))

// Pagination
const limit = Math.min(req.query.limit || 10, 100)
const offset = (req.query.page || 0) * limit
```

## Key Concepts

- RESTful design
- GraphQL schema design
- Error handling
- Authentication
- Rate limiting
- Versioning
- Documentation (OpenAPI, GraphQL SDL)
- Caching strategies
