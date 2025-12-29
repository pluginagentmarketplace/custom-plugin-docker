<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=600&height=100&lines=Docker+Assistant;8+Agents+%7C+12+Skills;Claude+Code+Plugin" alt="Docker Assistant" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-2.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-docker/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agents](https://img.shields.io/badge/Agents-8-orange?style=flat-square&logo=robot)](#-agents)
[![Skills](https://img.shields.io/badge/Skills-12-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-4-green?style=flat-square&logo=terminal)](#-commands)

<br/>

<!-- Quick CTA Row -->
[📦 **Install Now**](#-quick-start) · [🤖 **Explore Agents**](#-agents) · [📖 **Documentation**](#-documentation) · [⭐ **Star this repo**](https://github.com/pluginagentmarketplace/custom-plugin-docker)

---

### What is this?

> **Docker Assistant** is a Claude Code plugin with **8 agents** and **12 skills** for docker development.

</div>

---

## 📑 Table of Contents

<details>
<summary>Click to expand</summary>

- [Quick Start](#-quick-start)
- [Features](#-features)
- [Agents](#-agents)
- [Skills](#-skills)
- [Commands](#-commands)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

</details>

---

## 🚀 Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription

### Installation (Choose One)

<details open>
<summary><strong>Option 1: From Marketplace (Recommended)</strong></summary>

```bash
# Step 1️⃣ Add the marketplace
/plugin add marketplace pluginagentmarketplace/custom-plugin-docker

# Step 2️⃣ Install the plugin
/plugin install docker-development-assistant@docker-assistant-marketplace

# Step 3️⃣ Restart Claude Code
# Close and reopen your terminal/IDE
```

</details>

<details>
<summary><strong>Option 2: Local Installation</strong></summary>

```bash
# Clone the repository
git clone https://github.com/pluginagentmarketplace/custom-plugin-docker.git
cd custom-plugin-docker

# Load locally
/plugin load .

# Restart Claude Code
```

</details>

### ✅ Verify Installation

After restart, you should see these agents:

```
docker-development-assistant:07-docker-security
docker-development-assistant:08-docker-production
docker-development-assistant:05-docker-networking-storage
docker-development-assistant:06-docker-registries
docker-development-assistant:04-docker-compose
... and 3 more
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **8 Agents** | Specialized AI agents for docker tasks |
| 🛠️ **12 Skills** | Reusable capabilities with Golden Format |
| ⌨️ **4 Commands** | Quick slash commands |
| 🔄 **SASMP v1.3.0** | Full protocol compliance |

---

## 🤖 Agents

### 8 Specialized Agents

| # | Agent | Purpose |
|---|-------|---------|
| 1 | **07-docker-security** | Master Docker security - image scanning, runtime security, s |
| 2 | **08-docker-production** | Master Docker in production - orchestration, monitoring, log |
| 3 | **05-docker-networking-storage** | Master Docker networking and storage - networks, volumes, bi |
| 4 | **06-docker-registries** | Master Docker registries - Docker Hub, private registries, i |
| 5 | **04-docker-compose** | Master Docker Compose - multi-container applications, servic |
| 6 | **02-docker-images** | Master Docker images - building with Dockerfile, layer optim |
| 7 | **03-docker-containers** | Master Docker containers - running, managing, debugging, and |
| 8 | **01-docker-fundamentals** | Master Docker fundamentals - containers vs VMs, installation |

---

## 🛠️ Skills

### Available Skills

| Skill | Description | Invoke |
|-------|-------------|--------|
| `docker-registries` | Master Docker registries - Docker Hub, private registries, t | `Skill("docker-development-assistant:docker-registries")` |
| `docker-security` | Master Docker security - image scanning, runtime security, s | `Skill("docker-development-assistant:docker-security")` |
| `docker-images` | Master Docker images - pulling, building, tagging, pushing,  | `Skill("docker-development-assistant:docker-images")` |
| `docker-devex` | Docker developer experience - hot reloading, debugging, test | `Skill("docker-development-assistant:docker-devex")` |
| `docker-volumes` | Master Docker volumes - data persistence, bind mounts, volum | `Skill("docker-development-assistant:docker-volumes")` |
| `docker-dockerfile` | Master Dockerfile - instructions, multi-stage builds, optimi | `Skill("docker-development-assistant:docker-dockerfile")` |
| `docker-networks` | Master Docker networks - bridge, host, overlay, custom netwo | `Skill("docker-development-assistant:docker-networks")` |
| `docker-orchestration` | Docker orchestration - Swarm, Kubernetes basics, scaling, an | `Skill("docker-development-assistant:docker-orchestration")` |
| `docker-cli` | Master Docker CLI - essential commands, flags, and productiv | `Skill("docker-development-assistant:docker-cli")` |
| `docker-compose` | Master Docker Compose - multi-container apps, service orches | `Skill("docker-development-assistant:docker-compose")` |
| ... | +2 more | See skills/ directory |

---

## ⌨️ Commands

| Command | Description |
|---------|-------------|
| `/docker-debug` | Debug Docker containers and troubleshoot issues |
| `/docker-compose-up` | Start Docker Compose services with health checks |
| `/docker-build` | Build Docker image with best practices |
| `/docker-check` | Check Docker installation, daemon status, and system health |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

---

## 📁 Project Structure

<details>
<summary>Click to expand</summary>

```
custom-plugin-docker/
├── 📁 .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── 📁 agents/              # 8 agents
├── 📁 skills/              # 12 skills (Golden Format)
├── 📁 commands/            # 4 commands
├── 📁 hooks/
├── 📄 README.md
├── 📄 CHANGELOG.md
└── 📄 LICENSE
```

</details>

---

## 📅 Metadata

| Field | Value |
|-------|-------|
| **Version** | 2.0.0 |
| **Last Updated** | 2025-12-29 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 8 |
| **Skills** | 12 |
| **Commands** | 4 |

---

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## ⚠️ Security

> **Important:** This repository contains third-party code and dependencies.
>
> - ✅ Always review code before using in production
> - ✅ Check dependencies for known vulnerabilities
> - ✅ Follow security best practices
> - ✅ Report security issues privately via [Issues](../../issues)

---

## 📝 License

Copyright © 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## 👥 Contributors

<table>
<tr>
<td align="center">
<strong>Dr. Umit Kacar</strong><br/>
Senior AI Researcher & Engineer
</td>
<td align="center">
<strong>Muhsin Elcicek</strong><br/>
Senior Software Architect
</td>
</tr>
</table>

---

<div align="center">

**Made with ❤️ for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

</div>
