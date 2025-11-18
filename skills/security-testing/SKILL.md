---
name: security-testing
description: Master application security, testing strategies, and QA best practices. Learn OWASP Top 10, secure coding, test automation, and quality assurance. Use when implementing security or testing measures.
---

# Security & Testing

Build secure applications and ensure quality through comprehensive testing.

## Quick Start

### OWASP Top 10 Prevention

#### 1. SQL Injection Prevention
```typescript
// WRONG - Vulnerable to SQL injection
const query = `SELECT * FROM users WHERE email = '${email}'`;

// CORRECT - Use parameterized queries
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [email]);
```

#### 2. XSS (Cross-Site Scripting) Prevention
```typescript
// WRONG - Vulnerable to XSS
function renderUserComment(comment: string) {
  return `<div>${comment}</div>`; // Unsafe!
}

// CORRECT - Escape output
import DOMPurify from 'dompurify';

function renderUserComment(comment: string) {
  const safe = DOMPurify.sanitize(comment);
  return `<div>${safe}</div>`;
}

// Better - Use framework escaping
export const CommentView = ({ comment }: Props) => {
  return <div>{comment}</div>; // React escapes by default
};
```

#### 3. Authentication/Session Management
```typescript
// Secure JWT handling
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

class AuthService {
  async register(email: string, password: string) {
    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Save to database
    return await User.create({ email, password: hashedPassword });
  }

  async login(email: string, password: string) {
    const user = await User.findOne({ email });

    // Verify password
    const valid = await bcrypt.compare(password, user.password);
    if (!valid) throw new Error('Invalid credentials');

    // Generate JWT with expiration
    const token = jwt.sign(
      { userId: user.id },
      process.env.JWT_SECRET,
      { expiresIn: '24h' }
    );

    return token;
  }

  verifyToken(token: string) {
    try {
      return jwt.verify(token, process.env.JWT_SECRET);
    } catch {
      throw new Error('Invalid token');
    }
  }
}
```

#### 4. Sensitive Data Exposure
```typescript
// WRONG - Logging sensitive data
console.log('User credentials:', email, password);

// CORRECT - Use environment variables for secrets
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;

// Mask sensitive data in logs
function maskEmail(email: string) {
  return email.replace(/^(.{2}).*(@.*)$/, '$1***$2');
}

// Encryption for stored data
import crypto from 'crypto';

function encryptSensitive(data: string) {
  const cipher = crypto.createCipher('aes-256-cbc', process.env.ENCRYPTION_KEY);
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return encrypted;
}
```

### Test Automation

#### Unit Tests
```typescript
import { describe, it, expect } from '@jest/globals';
import { calculateTotal } from './cart';

describe('Cart calculations', () => {
  it('should calculate total correctly', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 20, quantity: 1 }
    ];
    const total = calculateTotal(items);
    expect(total).toBe(40);
  });

  it('should handle empty cart', () => {
    expect(calculateTotal([])).toBe(0);
  });

  it('should apply discount', () => {
    const items = [{ price: 100, quantity: 1 }];
    const total = calculateTotal(items, 0.1); // 10% discount
    expect(total).toBe(90);
  });
});
```

#### Integration Tests
```typescript
import supertest from 'supertest';
import { app } from './app';

describe('User API', () => {
  const request = supertest(app);

  it('should create a user', async () => {
    const response = await request.post('/users').send({
      email: 'test@example.com',
      password: 'secure123'
    });

    expect(response.status).toBe(201);
    expect(response.body.email).toBe('test@example.com');
  });

  it('should retrieve created user', async () => {
    const response = await request.get('/users/1');

    expect(response.status).toBe(200);
    expect(response.body.email).toBe('test@example.com');
  });
});
```

#### E2E Tests
```typescript
import { test, expect } from '@playwright/test';

test('user can login and view profile', async ({ page }) => {
  // Navigate to login
  await page.goto('http://localhost:3000/login');

  // Fill login form
  await page.fill('[name="email"]', 'user@example.com');
  await page.fill('[name="password"]', 'password123');

  // Submit
  await page.click('button[type="submit"]');

  // Verify redirect to profile
  await expect(page).toHaveURL('http://localhost:3000/profile');

  // Verify content
  await expect(page.locator('h1')).toContainText('User Profile');
});
```

### Code Review Checklist
```markdown
## Security Review
- [ ] No hardcoded secrets or API keys
- [ ] Input validation on all endpoints
- [ ] Output encoding for HTML/SQL
- [ ] HTTPS/TLS enabled
- [ ] Authentication required
- [ ] Authorization checks present
- [ ] CORS properly configured

## Code Quality
- [ ] Code follows style guide
- [ ] No unused imports/variables
- [ ] Proper error handling
- [ ] Meaningful variable names
- [ ] Comments for complex logic
- [ ] DRY principle applied
- [ ] No code duplication

## Performance
- [ ] No N+1 queries
- [ ] Appropriate caching
- [ ] Efficient algorithms
- [ ] Database indexes present

## Testing
- [ ] Tests added for new code
- [ ] Edge cases covered
- [ ] Tests passing locally
```

## Key Concepts

### Application Security
- **Defense in depth**: Multiple security layers
- **Principle of least privilege**: Grant minimum needed access
- **Secure by default**: Security built in, not added later
- **Input validation**: Never trust user input

### Testing Pyramid
```
         E2E Tests
        (10-20%)
       /
      Integration Tests
      (20-30%)
    /
Unit Tests (50-60%)
```

### QA Metrics
- **Code coverage**: Lines tested / Total lines
- **Defect density**: Bugs found / Lines of code
- **Test execution time**: CI/CD feedback speed
- **Coverage types**: Statement, branch, path coverage

## Best Practices

1. **Test-driven development** - Write tests first
2. **Comprehensive coverage** - Aim for 80%+ coverage
3. **Secure coding** - OWASP Top 10 prevention
4. **Code reviews** - Peer review all changes
5. **Automated testing** - Run tests in CI/CD
6. **Security scanning** - SAST/DAST tools
7. **Dependency scanning** - Track vulnerable libraries
8. **Continuous improvement** - Learn from bugs

## Tools & Libraries

**Testing**: Jest, Mocha, Pytest, Vitest
**E2E**: Playwright, Cypress, Selenium
**Security Scanning**: SNYK, SonarQube, Burp Suite
**Code Coverage**: Istanbul, Coverage.py
**API Testing**: Postman, REST Client, Thunder Client
