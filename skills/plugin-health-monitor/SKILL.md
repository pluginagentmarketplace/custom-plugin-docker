---
name: plugin-health-monitor
description: Continuous health monitoring and scoring with 5-factor weighted algorithm for Claude Code plugins
sasmp_version: "1.3.0"
bonded_agent: plugin-health-agent
bond_type: PRIMARY_BOND
---

# Plugin Health Monitor Skill

Continuous health monitoring and scoring system for Claude Code plugins using a 5-factor weighted algorithm.

## Purpose

Calculate health scores (0-100), monitor plugin structure, syntax, MCP connectivity, component loading, and track error history with stability metrics.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| plugin_path | string | Yes | - | Path to plugin directory |
| check_type | enum | No | full | full/quick/structure/syntax |
| threshold_warning | number | No | 85 | Warning threshold |
| threshold_critical | number | No | 70 | Critical threshold |
| include_history | boolean | No | true | Include error history |

## Health Score Algorithm

### 5-Factor Weighted Model

```python
def calculate_health_score(plugin):
    """
    Calculate plugin health score (0-100).

    Weights:
    - Structure validity: 25%
    - Syntax correctness: 20%
    - MCP connectivity: 15%
    - Component loading: 25%
    - Stability (no recent errors): 15%
    """
    scores = {
        'structure': check_structure(plugin),      # 25%
        'syntax': check_syntax(plugin),            # 20%
        'mcp': check_mcp_connection(plugin),       # 15%
        'loading': check_components_loaded(plugin), # 25%
        'stability': check_error_history(plugin),  # 15%
    }

    weights = [0.25, 0.20, 0.15, 0.25, 0.15]
    return sum(s * w for s, w in zip(scores.values(), weights))
```

### Factor Details

#### 1. Structure Validity (25%)

```bash
# Validation checks
ls -la plugin/.claude-plugin/                    # Directory exists?
cat plugin/.claude-plugin/plugin.json | jq .     # Valid JSON?
ls -d plugin/{agents,skills,commands,hooks}      # Required dirs?
```

**Scoring:**
- 100: All required directories and files present
- 75: Missing optional components
- 50: Missing some required files
- 0: Critical structure issues (E001)

#### 2. Syntax Correctness (20%)

```bash
# Check YAML frontmatter
grep -l "^>---" agents/*.md skills/*/SKILL.md

# Check JSON validity
jq . plugin/.claude-plugin/plugin.json

# Check markdown structure
head -20 agents/*.md | grep -E "^---"
```

**Scoring:**
- 100: All files have valid syntax
- 75: Minor syntax warnings
- 50: Some files have E102/E103 errors
- 0: Critical syntax failures

#### 3. MCP Connectivity (15%)

```bash
# Check for shell expansions (E201)
grep -rE '\$\(|\$\{|\$HOME|~/' --include="*.json" .

# Verify MCP server paths
cat plugin/hooks/hooks.json | jq '.mcp_servers[]?'
```

**Scoring:**
- 100: No shell expansions, valid paths
- 75: Minor path issues
- 50: E201 errors detected
- 0: MCP configuration broken

#### 4. Component Loading (25%)

```bash
# Verify all agents discoverable
ls agents/*.md | wc -l

# Verify all skills accessible
ls skills/*/SKILL.md | wc -l

# Check commands registered
ls commands/*.md | wc -l
```

**Scoring:**
- 100: All components load successfully
- 75: Some components have warnings
- 50: Loading errors present
- 0: Critical loading failures

#### 5. Stability (15%)

**Metrics tracked:**
- Errors in last 24 hours
- Repeated failures
- Critical errors ever
- Performance consistency

**Scoring:**
- 100: No issues in last 7 days
- 75: Minor issues, self-resolved
- 50: Recurring issues
- 0: Critical instability

## Health Status Thresholds

| Score | Status | Badge | Action |
|-------|--------|-------|--------|
| 85-100 | HEALTHY | GREEN | Continue monitoring |
| 70-84 | WARNING | YELLOW | Investigate, log issues |
| 50-69 | CRITICAL | ORANGE | Auto-heal or escalate |
| < 50 | FAILING | RED | Immediate intervention |

## Health Dashboard Output

```
PLUGIN HEALTH REPORT: my-plugin
================================================

Overall Score: 92/100 [HEALTHY]

Component Scores:
  Structure:  100/100 [OK] (25% weight)
  Syntax:      95/100 [OK] (20% weight)
  MCP:         85/100 [WARN] (15% weight)
  Loading:    100/100 [OK] (25% weight)
  Stability:   80/100 [WARN] (15% weight)

Recent Issues:
  - 2 minor warnings in last 24h
  - MCP connection intermittent (E201)

Recommendations:
  1. Fix shell expansion in hooks.json (E201)
  2. Monitor MCP connectivity
  3. Clear cache if issues persist

Last Check: 2025-12-30 14:23:45
Next Check: 2025-12-30 15:23:45
```

## Quick Health Check Script

```bash
#!/bin/bash
# quick-health-check.sh

PLUGIN_DIR="$1"
SCORE=100

echo "Plugin Health Check: $PLUGIN_DIR"
echo "================================"

# Structure check (-25 if fails)
if [ ! -d "$PLUGIN_DIR/.claude-plugin" ]; then
    echo "[FAIL] .claude-plugin directory missing"
    SCORE=$((SCORE - 25))
else
    echo "[PASS] .claude-plugin directory exists"
fi

# Syntax check (-20 if fails)
if grep -rq "^>---" "$PLUGIN_DIR/agents/" 2>/dev/null; then
    echo "[FAIL] Malformed YAML frontmatter detected (E102)"
    SCORE=$((SCORE - 20))
else
    echo "[PASS] YAML frontmatter valid"
fi

# MCP check (-15 if fails)
if grep -rqE '\$HOME|~/' "$PLUGIN_DIR" --include="*.json" 2>/dev/null; then
    echo "[FAIL] Shell expansions detected (E201)"
    SCORE=$((SCORE - 15))
else
    echo "[PASS] No shell expansions"
fi

echo "================================"
echo "Health Score: $SCORE/100"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `plugin_path not found` | Invalid path | Verify path exists |
| `permission denied` | Access issues | Check file permissions |
| `json parse error` | Malformed JSON | Run JSON validator |

## Usage

```
Skill("plugin-health-monitor")
```

## Assets

- `assets/health-config.yaml` - Threshold configuration
- `assets/health-schema.json` - Output schema
- `scripts/health-check.py` - Python health checker
- `references/HEALTH-GUIDE.md` - Detailed health documentation

## Related Skills

- plugin-troubleshooter (diagnosis)
- plugin-recovery-specialist (fix actions)
