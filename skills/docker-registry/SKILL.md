---
name: docker-registry
description: Private registry setup and image management
sasmp_version: "1.3.0"
bonded_agent: 02-docker-images
bond_type: PRIMARY_BOND
---

# Docker Registry Skill

Set up and manage private Docker registries for secure image distribution.

## What This Skill Provides

- Private registry deployment
- Image push/pull operations
- Authentication and access control
- Registry backup and maintenance
- Multi-registry management

## Assets

- `registry-config.yaml` - Registry configuration templates
- `docker-compose-registry.yaml` - Quick registry deployment

## Scripts

- `registry-setup.sh` - Automated registry installation
- `image-sync.sh` - Sync images between registries

## References

- `REGISTRY-GUIDE.md` - Complete registry documentation
