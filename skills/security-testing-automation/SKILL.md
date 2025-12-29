---
name: security-testing-automation
description: Master web security, OWASP Top 10, testing automation, and quality assurance practices.
sasmp_version: "1.3.0"
bonded_agent: 01-frontend-web-development
bond_type: PRIMARY_BOND
---

# Security & Testing Automation

Application security and quality.

## OWASP Top 10

- SQL injection prevention
- Cross-site scripting (XSS) 
- CSRF protection
- Authentication/Authorization
- Sensitive data exposure
- XXE prevention
- Broken access control
- Security misconfiguration
- Deserialization attacks
- Logging gaps

## Test Automation

```typescript
describe('Login', () => {
  it('should login with valid credentials', () => {
    cy.visit('/')
    cy.get('[data-testid=email]').type('user@example.com')
    cy.get('[data-testid=password]').type('password')
    cy.get('button').click()
    cy.url().should('include', '/dashboard')
  })
})
```

## Key Skills

- Secure coding
- Penetration testing
- Test-driven development
- Security scanning
