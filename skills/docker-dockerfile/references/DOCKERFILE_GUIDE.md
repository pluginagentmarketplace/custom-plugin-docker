# Dockerfile Best Practices

## Instruction Order

```dockerfile
# 1. Base image (rarely changes)
FROM node:20-alpine

# 2. System deps (rarely changes)
RUN apk add --no-cache curl

# 3. App deps (changes sometimes)
COPY package*.json ./
RUN npm ci

# 4. App code (changes often)
COPY . .

# 5. Runtime config
CMD ["node", "app.js"]
```

## CMD vs ENTRYPOINT

| | CMD | ENTRYPOINT |
|-|-----|------------|
| Override | Easy | Requires --entrypoint |
| Use | Default args | Fixed command |

## ARG vs ENV

- ARG: Build-time only
- ENV: Build + runtime
