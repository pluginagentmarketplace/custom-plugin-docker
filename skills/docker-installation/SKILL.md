---
name: docker-installation
description: Complete Docker installation guide for Linux, macOS, Windows with Docker Desktop and Docker Engine options
sasmp_version: "1.3.0"
bonded_agent: docker-fundamentals
bond_type: PRIMARY_BOND
---

# Docker Installation Skill

## Linux (Ubuntu/Debian)

```bash
# Remove old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

# Install prerequisites
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg

# Add Docker GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

## macOS

```bash
# Download Docker Desktop from docker.com
# Or use Homebrew
brew install --cask docker
```

## Windows

1. Enable WSL2
2. Download Docker Desktop
3. Install and configure

## Verification

```bash
docker --version
docker run hello-world
docker compose version
```

## Assets
- `install-docker.sh` - Cross-platform installer

## References
- `INSTALLATION_GUIDE.md` - Detailed guide
