# Docker Registry Guide

## Registry Comparison

| Registry | Free Tier | Private |
|----------|-----------|---------|
| Docker Hub | 1 private | Yes |
| GHCR | Unlimited | Yes |
| ECR | 500MB | Yes |
| GCR | 500MB | Yes |

## Tagging Best Practices

1. Use semantic versions (v1.2.3)
2. Include git SHA for traceability
3. Avoid :latest in production
4. Use immutable tags
