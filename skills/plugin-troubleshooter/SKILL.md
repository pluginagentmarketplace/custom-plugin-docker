---
name: plugin-troubleshooter
description: Deep diagnosis and root cause analysis for Claude Code plugin issues with 45+ error code patterns
sasmp_version: "1.3.0"
bonded_agent: plugin-health-agent
bond_type: PRIMARY_BOND
---

# Plugin Troubleshooter Skill

Deep diagnosis and root cause analysis system that maps symptoms to error codes (E001-E802) for comprehensive plugin troubleshooting.

## Purpose

Analyze logs, configs, and structure to identify issues, map symptoms to specific error codes, and propose targeted fixes.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| plugin_path | string | Yes | - | Path to plugin directory |
| symptom | string | No | - | Reported symptom description |
| error_codes | array | No | [] | Specific codes to check |
| deep_scan | boolean | No | false | Enable thorough analysis |
| include_logs | boolean | No | true | Analyze log files |

## Diagnostic Flow

```
SYMPTOM --> ERROR CODE --> ROOT CAUSE --> FIX PROPOSAL
   |            |              |              |
   v            v              v              v
"Agent not   E102        Malformed     "Replace >---
 loading"              frontmatter     with ---"
```

## Error Code Detection Matrix

### Structural Errors (E001-E099)

| Code | Detection | Auto-Fix | Risk |
|------|-----------|----------|------|
| E001 | `.claude-plugin` is file not dir | YES | LOW |
| E002 | Missing `plugin.json` | YES | LOW |
| E003 | Invalid `plugin.json` schema | YES | LOW |
| E004 | Missing agents directory | YES | LOW |
| E005 | Missing skills directory | YES | LOW |
| E006 | Missing commands directory | YES | LOW |
| E007 | Missing hooks directory | YES | LOW |
| E008 | Incorrect file permissions | YES | LOW |
| E009 | Symlink resolution failure | PARTIAL | MEDIUM |
| E010 | Path traversal vulnerability | NO | HIGH |

### Syntax Errors (E101-E199)

| Code | Detection | Auto-Fix | Risk |
|------|-----------|----------|------|
| E101 | Missing YAML frontmatter | YES | LOW |
| E102 | Malformed frontmatter (`>---`) | YES | LOW |
| E103 | Missing required YAML fields | YES | LOW |
| E104 | Invalid YAML syntax | PARTIAL | LOW |
| E105 | Invalid JSON in config | YES | LOW |
| E106 | Markdown syntax errors | NO | LOW |
| E107 | Encoding issues (non-UTF8) | YES | LOW |
| E108 | BOM character detected | YES | LOW |
| E109 | Trailing whitespace issues | YES | LOW |
| E110 | Line ending inconsistency | YES | LOW |
| E111 | Tab/space mixing | YES | LOW |

### Runtime Errors (E201-E299)

| Code | Detection | Auto-Fix | Risk |
|------|-----------|----------|------|
| E201 | Shell expansion in MCP | PARTIAL | HIGH |
| E202 | Environment variable missing | NO | MEDIUM |
| E203 | Path not absolute | YES | MEDIUM |
| E204 | Binary not found | NO | HIGH |
| E205 | Permission denied | YES | MEDIUM |
| E206 | Resource exhaustion | NO | HIGH |

### Naming Errors (E301-E399)

| Code | Detection | Auto-Fix | Risk |
|------|-----------|----------|------|
| E301 | Invalid plugin name chars | YES | LOW |
| E302 | Reserved name usage | YES | LOW |
| E303 | Name collision (plugin=marketplace) | YES | LOW |
| E304 | Duplicate agent names | YES | LOW |

### Validation Errors (E401-E499)

| Code | Detection | Auto-Fix | Risk |
|------|-----------|----------|------|
| E401 | Skill subdirectory violation | YES | MEDIUM |
| E402 | Missing required asset | YES | MEDIUM |
| E403 | Missing command frontmatter | YES | LOW |
| E404 | Invalid hook configuration | PARTIAL | MEDIUM |
| E405 | Circular skill dependency | NO | MEDIUM |
| E406 | Orphan file (not referenced) | NO | LOW |
| E407 | Version mismatch | YES | MEDIUM |
| E408 | Schema validation failure | PARTIAL | MEDIUM |
| E409 | Invalid bond type | YES | LOW |
| E410 | Missing bond reference | YES | LOW |

## Detection Scripts

### E102: Malformed YAML Frontmatter

```bash
#!/bin/bash
# detect-e102.sh

PLUGIN_DIR="$1"
echo "Checking E102: Malformed YAML Frontmatter"
echo "=========================================="

# Find all markdown files with >--- instead of ---
ERRORS=$(grep -rl "^>---" "$PLUGIN_DIR/agents/" "$PLUGIN_DIR/skills/" 2>/dev/null)

if [ -n "$ERRORS" ]; then
    echo "E102 DETECTED in:"
    echo "$ERRORS"
    echo ""
    echo "Fix: Replace '>---' with '---' at line 1"
    exit 1
else
    echo "No E102 errors found"
    exit 0
fi
```

### E201: Shell Expansion Bug

```bash
#!/bin/bash
# detect-e201.sh

PLUGIN_DIR="$1"
echo "Checking E201: Shell Expansion in MCP Config"
echo "============================================="

# Patterns that cause MCP issues
PATTERNS='(\$\(|\$\{|\$HOME|\$USER|~/|`)'

ERRORS=$(grep -rE "$PATTERNS" "$PLUGIN_DIR" --include="*.json" 2>/dev/null)

if [ -n "$ERRORS" ]; then
    echo "E201 DETECTED:"
    echo "$ERRORS"
    echo ""
    echo "Fix: Replace shell expansions with absolute paths"
    exit 1
else
    echo "No E201 errors found"
    exit 0
fi
```

### E303: Name Collision

```bash
#!/bin/bash
# detect-e303.sh

PLUGIN_DIR="$1"
echo "Checking E303: Name Collision"
echo "=============================="

PLUGIN_NAME=$(jq -r '.name' "$PLUGIN_DIR/.claude-plugin/plugin.json" 2>/dev/null)
MARKET_NAME=$(jq -r '.name' "$PLUGIN_DIR/.claude-plugin/marketplace.json" 2>/dev/null)

if [ "$PLUGIN_NAME" = "$MARKET_NAME" ]; then
    echo "E303 DETECTED!"
    echo "Plugin name: $PLUGIN_NAME"
    echo "Marketplace name: $MARKET_NAME"
    echo ""
    echo "Fix: Rename marketplace to ${PLUGIN_NAME}-marketplace"
    exit 1
else
    echo "No E303 errors found"
    exit 0
fi
```

### E401: Skill Subdirectory Violation

```bash
#!/bin/bash
# detect-e401.sh

PLUGIN_DIR="$1"
echo "Checking E401: Skill Subdirectory Violation"
echo "============================================"

VIOLATIONS=0

for skill_dir in "$PLUGIN_DIR/skills"/*/; do
    for subdir in assets scripts references; do
        subdir_path="$skill_dir$subdir"
        if [ -d "$subdir_path" ]; then
            # Count real files (not .gitkeep or tiny README)
            real_files=$(find "$subdir_path" -type f ! -name ".gitkeep" -size +100c | wc -l)
            if [ "$real_files" -eq 0 ]; then
                echo "E401: $subdir_path (placeholder only)"
                VIOLATIONS=$((VIOLATIONS + 1))
            fi
        fi
    done
done

if [ $VIOLATIONS -gt 0 ]; then
    echo ""
    echo "Total E401 violations: $VIOLATIONS"
    exit 1
else
    echo "No E401 errors found"
    exit 0
fi
```

## Troubleshooting Flowcharts

### Agent Not Loading

```
Agent Not Loading?
|
+-- Check file exists
|   +-- NO --> Create agent file
|   +-- YES --> Continue
|
+-- Check YAML frontmatter
|   +-- Missing --> E101
|   +-- Malformed (>---) --> E102
|   +-- Missing fields --> E103
|   +-- Valid --> Continue
|
+-- Check plugin.json reference
|   +-- Missing --> Add to agents array
|   +-- Present --> Continue
|
+-- Check permissions
    +-- Not readable --> E008
    +-- Readable --> Deep investigation needed
```

### Skill Not Accessible

```
Skill Not Accessible?
|
+-- Check SKILL.md exists
|   +-- NO --> E701
|   +-- Size < 200 bytes --> E701
|   +-- YES --> Continue
|
+-- Check subdirectories
|   +-- assets/ placeholder --> E702
|   +-- scripts/ placeholder --> E703
|   +-- references/ placeholder --> E704
|
+-- Check bonding
|   +-- No bonded_agent --> E502
|   +-- Invalid bond_type --> E409
|
+-- Check SASMP fields
    +-- Missing sasmp_version --> E501
```

## Diagnosis Report Format

```
TROUBLESHOOTING REPORT
======================
Plugin: my-plugin
Scan Type: Deep Scan
Timestamp: 2025-12-30 14:30:00

ERRORS FOUND: 3

[E102] Malformed YAML Frontmatter
  File: agents/my-agent.md
  Line: 1
  Found: '>---'
  Expected: '---'
  Auto-Fix: YES
  Risk: LOW

[E201] Shell Expansion in MCP Config
  File: hooks/hooks.json
  Line: 15
  Found: '$HOME/.local/bin'
  Expected: '/home/user/.local/bin'
  Auto-Fix: PARTIAL (needs user input)
  Risk: HIGH

[E401] Skill Subdirectory Violation
  File: skills/my-skill/assets/
  Issue: Contains only README.md
  Expected: Real asset files
  Auto-Fix: YES (with templates)
  Risk: MEDIUM

RECOMMENDATIONS:
1. Run golden-format-fixer for E401
2. Manually fix E201 (requires absolute path)
3. Run YAML fixer for E102

ESTIMATED FIX TIME: 5 minutes
AUTO-FIXABLE: 2/3 errors
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `plugin not found` | Invalid path | Verify plugin exists |
| `permission denied` | Access issues | Run with proper permissions |
| `parse error` | Corrupted file | Restore from backup |

## Usage

```
Skill("plugin-troubleshooter")
```

## Assets

- `assets/error-codes.yaml` - Complete error code database
- `assets/symptom-map.json` - Symptom to error code mapping
- `scripts/diagnose.py` - Diagnosis automation script
- `references/TROUBLESHOOTING-GUIDE.md` - Detailed troubleshooting docs

## Related Skills

- plugin-health-monitor (detection)
- plugin-recovery-specialist (fixes)
- golden-format-validator (E701-E704)
