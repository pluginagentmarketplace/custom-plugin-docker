---
name: docker-multi-stage
description: Multi-stage builds for optimized production images
sasmp_version: "1.3.0"
bonded_agent: 02-docker-images
bond_type: SECONDARY_BOND
---

# Docker Multi-Stage Builds Skill

Create optimized, minimal production images using multi-stage builds.

## What This Skill Provides

- Multi-stage Dockerfile patterns
- Build optimization techniques
- Layer caching strategies
- Production image minimization
- Language-specific templates

## Assets

- `multistage-templates/` - Templates for Node, Python, Go, Java
- `optimization-checklist.yaml` - Image optimization checklist

## Scripts

- `image-size-analyzer.sh` - Analyze and compare image sizes

## References

- `MULTISTAGE-PATTERNS.md` - Common multi-stage patterns
