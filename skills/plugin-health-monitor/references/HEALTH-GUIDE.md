# Plugin Health Monitoring Guide

Comprehensive documentation for understanding and using the plugin health monitoring system.

## Overview

The Plugin Health Monitor uses a **5-factor weighted scoring algorithm** to calculate plugin health on a scale of 0-100.

## Health Score Factors

### 1. Structure Validity (25%)

Validates the plugin directory structure:

```
plugin/
├── .claude-plugin/
│   ├── plugin.json      (required)
│   └── marketplace.json (optional)
├── agents/              (required)
├── skills/              (required)
├── commands/            (required)
├── hooks/               (required)
└── README.md            (required)
```

**Scoring:**
- 100: All required components present
- 75: Missing optional components
- 50: Missing some required directories
- 0: Critical structure failure (E001)

### 2. Syntax Correctness (20%)

Validates YAML, JSON, and Markdown syntax:

- YAML frontmatter in agent/skill files
- Valid JSON in plugin.json, hooks.json
- Proper markdown structure

**Common Errors:**
- E101: Missing YAML frontmatter
- E102: Malformed frontmatter (>--- instead of ---)
- E103: Missing required YAML fields
- E105: Invalid JSON syntax

### 3. MCP Connectivity (15%)

Checks MCP configuration for issues:

- No shell expansions ($HOME, ~/, etc.)
- Valid absolute paths
- Proper server configuration

**Critical Error:**
- E201: Shell expansion in MCP config (causes runtime failures)

### 4. Component Loading (25%)

Verifies all components can be loaded:

- All agents discoverable
- All skills accessible
- All commands registered
- No loading errors

### 5. Stability (15%)

Tracks error history and stability:

- Errors in last 24/168 hours
- Repeated failures
- Critical error history

## Health Status Thresholds

| Score Range | Status | Color | Action Required |
|-------------|--------|-------|-----------------|
| 85-100 | HEALTHY | Green | Continue monitoring |
| 70-84 | WARNING | Yellow | Investigate issues |
| 50-69 | CRITICAL | Orange | Auto-heal or escalate |
| 0-49 | FAILING | Red | Immediate intervention |

## Running Health Checks

### Quick Check

```bash
python scripts/health-check.py /path/to/plugin
```

### Detailed Report

```bash
python scripts/health-check.py /path/to/plugin --verbose
```

### JSON Output

```bash
python scripts/health-check.py /path/to/plugin --format json
```

## Interpreting Results

### Healthy Plugin Example

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

No issues detected!
```

### Plugin with Issues Example

```
PLUGIN HEALTH REPORT: my-plugin
================================

Overall Score: 72/100 [WARNING]

Component Scores:
  Structure:   80/100 [WARN]
  Syntax:      60/100 [WARN]
  MCP:         70/100 [WARN]
  Loading:    100/100 [OK]
  Stability:   80/100 [OK]

Issues Found: 3

  [E102] Malformed YAML frontmatter
    File: agents/my-agent.md
    Severity: LOW
    Auto-fixable: Yes

  [E201] Shell expansion detected: $HOME
    File: hooks/hooks.json
    Severity: HIGH
    Auto-fixable: No

  [E401] Placeholder only in assets/
    File: skills/my-skill/assets/
    Severity: MEDIUM
    Auto-fixable: Yes
```

## Auto-Healing

When issues are detected with `auto_fixable: Yes`, use the recovery tools:

```bash
# Fix Golden Format issues
Skill("golden-format-fixer")

# Fix syntax issues
python scripts/fix-syntax.py /path/to/plugin

# Full recovery
Skill("plugin-recovery-specialist")
```

## Best Practices

1. **Regular Monitoring**: Run health checks after every significant change
2. **Pre-publish Validation**: Always validate before publishing to marketplace
3. **Fix Incrementally**: Address issues one category at a time
4. **Keep Backups**: Enable automatic backups for rollback capability
5. **Document Fixes**: Log all fixes for future reference

## Integration with CI/CD

```yaml
# Example GitHub Action
- name: Plugin Health Check
  run: |
    python scripts/health-check.py . --format json > health-report.json
    SCORE=$(jq '.health_score' health-report.json)
    if [ "$SCORE" -lt 85 ]; then
      echo "Health check failed: $SCORE/100"
      exit 1
    fi
```

## Troubleshooting

### Score Suddenly Dropped

1. Check recent changes (`git diff`)
2. Run detailed health check
3. Review error codes
4. Apply fixes or rollback

### Cannot Identify Issue

1. Enable verbose logging
2. Check component-by-component
3. Use plugin-troubleshooter skill
4. Review error code documentation

## Related Resources

- [Error Codes Reference](../../../references/ERROR-CODES.md)
- [Golden Format Guide](../../golden-format-validator/references/GOLDEN-FORMAT-GUIDE.md)
- [Recovery Procedures](../../plugin-recovery-specialist/references/RECOVERY-GUIDE.md)
