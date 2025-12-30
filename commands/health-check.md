---
description: Run comprehensive plugin health check with 5-factor weighted scoring
allowed-tools: Read, Bash, Glob, Grep
---

# /health-check Command

Run a comprehensive health check on your Claude Code plugin using the 5-factor weighted scoring algorithm.

## Usage

```
/health-check [plugin_path]
```

## What It Does

1. **Structure Check (25%)**: Validates directory structure and required files
2. **Syntax Check (20%)**: Validates YAML frontmatter and JSON syntax
3. **MCP Check (15%)**: Detects shell expansions and configuration issues
4. **Loading Check (25%)**: Verifies all components can be loaded
5. **Stability Check (15%)**: Reviews error history and stability

## Output

```
PLUGIN HEALTH REPORT: my-plugin
================================

Overall Score: 92/100 [HEALTHY]

Component Scores:
  Structure:  100/100 [OK]
  Syntax:      95/100 [OK]
  MCP:         85/100 [WARN]
  Loading:    100/100 [OK]
  Stability:   80/100 [OK]

Issues Found: 2
  [E201] Shell expansion in hooks.json
  [E401] Placeholder only in skills/api/assets/

Recommendations:
  1. Replace $HOME with absolute path
  2. Run golden-format-fixer
```

## Health Status

| Score | Status | Action |
|-------|--------|--------|
| 85-100 | HEALTHY | Continue monitoring |
| 70-84 | WARNING | Investigate issues |
| 50-69 | CRITICAL | Auto-heal or escalate |
| < 50 | FAILING | Immediate intervention |

## Related Commands

- `/diagnose` - Deep error diagnosis
- `/fix-golden-format` - Fix Golden Format issues
- `/validate-structure` - Validate plugin structure
