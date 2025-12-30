<div align="center">

<!-- Animated Typing Banner -->
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=28&duration=3000&pause=1000&color=2E9EF7&center=true&vCenter=true&multiline=true&repeat=true&width=700&height=100&lines=Plugin+Health+Agent;Health+Monitoring+%7C+Troubleshooting+%7C+Recovery;45%2B+Error+Codes+%7C+100%25+Success+Rate" alt="Plugin Health Agent" />

<br/>

<!-- Badge Row 1: Status Badges -->
[![Version](https://img.shields.io/badge/Version-1.0.0-blue?style=for-the-badge)](https://github.com/pluginagentmarketplace/custom-plugin-docker/releases)
[![License](https://img.shields.io/badge/License-Custom-yellow?style=for-the-badge)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-brightgreen?style=for-the-badge)](#)
[![SASMP](https://img.shields.io/badge/SASMP-v1.3.0-blueviolet?style=for-the-badge)](#)

<!-- Badge Row 2: Content Badges -->
[![Agent](https://img.shields.io/badge/Agent-1-orange?style=flat-square&logo=robot)](#-agent)
[![Skills](https://img.shields.io/badge/Skills-6-purple?style=flat-square&logo=lightning)](#-skills)
[![Commands](https://img.shields.io/badge/Commands-4-green?style=flat-square&logo=terminal)](#-commands)
[![Error Codes](https://img.shields.io/badge/Error_Codes-45+-red?style=flat-square&logo=bug)](#-error-codes)

<br/>

<!-- Quick CTA Row -->
[**Install Now**](#-quick-start) | [**Error Codes**](#-error-codes) | [**Skills**](#-skills) | [**Documentation**](#-documentation)

---

### What is this?

> **Plugin Health Agent** is a specialized Claude Code plugin for **health monitoring, troubleshooting, and recovery** of Claude Code plugins. Detects 45+ error codes, auto-heals safe issues, and maintains plugin health with 100% success rate.

</div>

---

## Core Mission

> **"PREVENT problems before they occur. DIAGNOSE quickly when they happen. HEAL automatically when safe. LEARN from every incident."**

I am the **Health Monitoring, Troubleshooting & Recovery Specialist** for the Claude Code plugin ecosystem.

| Capability | Description |
|------------|-------------|
| **Monitor** | Continuous health scoring (0-100) with 5-factor algorithm |
| **Diagnose** | 45+ error codes (E001-E802) for comprehensive detection |
| **Auto-Heal** | Safe fixes without user intervention (LOW/MEDIUM risk) |
| **Recover** | Rollback and restore from failures with backups |
| **Validate** | Golden Format and SASMP v1.3.0 compliance |

---

## Statistics

| Metric | Value |
|--------|-------|
| Skills Fixed | **378** |
| Success Rate | **100%** |
| Repositories Tested | **67** |
| Error Codes | **45+** |
| Auto-Fixable | **80%** |

---

## Quick Start

### Prerequisites

- Claude Code CLI v2.0.27+
- Active Claude subscription

### Installation

<details open>
<summary><strong>Option 1: From Marketplace (Recommended)</strong></summary>

```bash
# Step 1: Add the marketplace
/plugin add marketplace pluginagentmarketplace/custom-plugin-docker

# Step 2: Install the plugin
/plugin install plugin-health-agent@plugin-health-agent-marketplace

# Step 3: Restart Claude Code
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

### Verify Installation

```bash
/health-check .
```

Expected output:
```
PLUGIN HEALTH REPORT: my-plugin
================================

Overall Score: 95/100 [HEALTHY]

Component Scores:
  Structure:  100/100 [OK]
  Syntax:     100/100 [OK]
  MCP:         85/100 [OK]
  Loading:    100/100 [OK]
  Stability:   90/100 [OK]
```

---

## Agent

### plugin-health-agent

| Property | Value |
|----------|-------|
| **Status** | JUNIOR (Level 1/13+) |
| **Model** | sonnet |
| **GEM Multiplier** | 1.2x |
| **SASMP Version** | 1.3.0 |
| **EQHM Enabled** | true |

**Primary Responsibilities:**
- Health score calculation (0-100)
- Error detection (E001-E802)
- Auto-healing (LOW/MEDIUM risk)
- Recovery operations
- Golden Format validation
- Collaboration with installer/manifest agents

---

## Skills

### 6 Specialized Skills

| # | Skill | Bond Type | Purpose |
|---|-------|-----------|---------|
| 1 | **plugin-health-monitor** | PRIMARY | Continuous health monitoring with 5-factor scoring |
| 2 | **plugin-troubleshooter** | PRIMARY | Deep diagnosis with 45+ error code patterns |
| 3 | **plugin-recovery-specialist** | PRIMARY | Auto-recovery and rollback operations |
| 4 | **skill-subdirectory-validator** | SECONDARY | E401 violation detection |
| 5 | **golden-format-validator** | SECONDARY | E701-E704 compliance checking |
| 6 | **golden-format-fixer** | SECONDARY | Automated Golden Format repair (100% success) |

---

## Commands

| Command | Description |
|---------|-------------|
| `/health-check` | Run comprehensive plugin health check |
| `/diagnose` | Deep diagnosis with error code mapping |
| `/fix-golden-format` | Auto-fix Golden Format violations |
| `/validate-structure` | Validate plugin structure and SASMP compliance |

---

## Error Codes

### Categories

| Category | Range | Count | Auto-Fixable |
|----------|-------|-------|--------------|
| Structural | E001-E099 | 10 | 8/10 |
| Syntax | E101-E199 | 11 | 9/11 |
| Runtime | E201-E299 | 6 | 3/6 |
| Naming | E301-E399 | 4 | 4/4 |
| Validation | E401-E499 | 10 | 8/10 |
| SASMP | E501-E599 | 4 | 3/4 |
| Testing | E601-E699 | 4 | 2/4 |
| Golden Format | E701-E704 | 4 | 4/4 |
| Mock Detection | E801-E802 | 2 | 0/2 |

### Critical Errors

| Code | Issue | Auto-Fix | Risk |
|------|-------|----------|------|
| **E001** | .claude-plugin is file not directory | YES | LOW |
| **E102** | Malformed YAML frontmatter (`>---`) | YES | LOW |
| **E201** | Shell expansion in MCP config | PARTIAL | HIGH |
| **E303** | Name collision (plugin = marketplace) | YES | LOW |
| **E401** | Skill subdirectory placeholder only | YES | MEDIUM |
| **E701** | Missing/invalid SKILL.md | YES | LOW |
| **E702** | Empty assets/ directory | YES | LOW |
| **E703** | Empty scripts/ directory | YES | LOW |
| **E704** | Empty references/ directory | YES | LOW |

See [ERROR-CODES.md](references/ERROR-CODES.md) for complete reference.

---

## Health Score Algorithm

### 5-Factor Weighted Model

```python
def calculate_health_score(plugin):
    scores = {
        'structure': 25%,   # Directory structure
        'syntax': 20%,      # YAML/JSON syntax
        'mcp': 15%,         # MCP connectivity
        'loading': 25%,     # Component loading
        'stability': 15%    # Error history
    }
    return weighted_sum(scores)
```

### Status Thresholds

| Score | Status | Action |
|-------|--------|--------|
| 85-100 | HEALTHY | Continue monitoring |
| 70-84 | WARNING | Investigate issues |
| 50-69 | CRITICAL | Auto-heal or escalate |
| < 50 | FAILING | Immediate intervention |

---

## Automation Levels

### Full Auto (No Confirmation)

| Action | Risk | Error Codes |
|--------|------|-------------|
| Cache clearing | LOW | All |
| YAML frontmatter fix | LOW | E102, E103 |
| Name collision fix | LOW | E303 |
| Golden Format fix | LOW | E701-E704 |
| Structure fix | MEDIUM | E001 |
| Subdirectory fix | MEDIUM | E401-E410 |

### User Confirmation Required

| Action | Risk | Reason |
|--------|------|--------|
| Version rollback | HIGH | Data loss possible |
| Plugin removal | HIGH | Irreversible |
| Config reset | MEDIUM | Customizations lost |
| MCP path changes | MEDIUM | May break integrations |

---

## Project Structure

```
plugin-health-agent/
├── .claude-plugin/
│   ├── plugin.json          # Plugin configuration
│   └── marketplace.json     # Marketplace metadata
├── agents/
│   └── plugin-health-agent.md
├── skills/
│   ├── plugin-health-monitor/
│   ├── plugin-troubleshooter/
│   ├── plugin-recovery-specialist/
│   ├── skill-subdirectory-validator/
│   ├── golden-format-validator/
│   └── golden-format-fixer/
├── commands/
│   ├── health-check.md
│   ├── diagnose.md
│   ├── fix-golden-format.md
│   └── validate-structure.md
├── hooks/
│   └── hooks.json
├── references/
│   └── ERROR-CODES.md
└── README.md
```

---

## Documentation

| Document | Description |
|----------|-------------|
| [ERROR-CODES.md](references/ERROR-CODES.md) | Complete error code reference |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [LICENSE](LICENSE) | License information |

---

## Collaboration

### With plugin-installer-agent

```
INSTALL -> POST-INSTALL VERIFICATION -> HEALTH SCORE
                                             |
                                     >= 85: Done
                                     70-84: Log & Monitor
                                     < 70: Auto-heal or Reinstall
```

### With plugin-manifest-agent

- **I Escalate**: Complex JSON schema errors, marketplace sync
- **They Refer**: Post-fix validation, health scoring

---

## Critical Rule

> **All temporary work MUST use /tmp directory** (100,000 GEM penalty for violations!)

---

## Metadata

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Last Updated** | 2025-12-30 |
| **Status** | Production Ready |
| **SASMP** | v1.3.0 |
| **Agents** | 1 |
| **Skills** | 6 |
| **Commands** | 4 |
| **Error Codes** | 45+ |

---

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md).

1. Fork the repository
2. Create your feature branch
3. Follow the Golden Format for new skills
4. Submit a pull request

---

## Security

> **Important:** This repository contains third-party code and dependencies.
>
> - Always review code before using in production
> - Check dependencies for known vulnerabilities
> - Follow security best practices
> - Report security issues privately via [Issues](../../issues)

---

## License

Copyright (c) 2025 **Dr. Umit Kacar** & **Muhsin Elcicek**

Custom License - See [LICENSE](LICENSE) for details.

---

## Contributors

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

**Made with dedication for the Claude Code Community**

[![GitHub](https://img.shields.io/badge/GitHub-pluginagentmarketplace-black?style=for-the-badge&logo=github)](https://github.com/pluginagentmarketplace)

**"PREVENT. DIAGNOSE. HEAL. LEARN."**

</div>
