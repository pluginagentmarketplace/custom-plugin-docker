---
name: docker-networks
description: Master Docker networks - bridge, host, overlay, custom networks, and container connectivity
sasmp_version: "1.3.0"
bonded_agent: docker-networking-storage
bond_type: PRIMARY_BOND
---

# Docker Networks Skill

## Network Types

| Type | Use Case |
|------|----------|
| bridge | Default, isolated |
| host | Direct host network |
| none | No networking |
| overlay | Swarm multi-host |

## Network Commands

```bash
docker network ls
docker network create mynet
docker network connect mynet container
docker network disconnect mynet container
docker network inspect mynet
docker network rm mynet
```

## Custom Bridge

```bash
docker network create --driver bridge mynet

docker run -d --network mynet --name db postgres
docker run -d --network mynet --name app myapp
# app can reach db by name
```

## Assets
- `network-setup.sh` - Network configuration

## References
- `NETWORK_GUIDE.md` - Best practices
