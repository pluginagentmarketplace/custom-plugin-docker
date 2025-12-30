---
description: Deep diagnosis of plugin issues with error code mapping (E001-E802)
allowed-tools: Read, Bash, Glob, Grep
---

# /diagnose Command

Perform deep diagnosis of plugin issues, mapping symptoms to specific error codes (E001-E802) with root cause analysis.

## Usage

```
/diagnose [plugin_path] [--symptom "description"]
```

## What It Does

1. **Symptom Analysis**: Maps reported symptoms to error codes
2. **Error Detection**: Scans for all 45+ error patterns
3. **Root Cause Analysis**: Identifies underlying causes
4. **Fix Proposals**: Suggests targeted solutions

## Error Code Categories

| Category | Range | Examples |
|----------|-------|----------|
| Structural | E001-E099 | Missing directories, wrong structure |
| Syntax | E101-E199 | YAML/JSON errors, encoding issues |
| Runtime | E201-E299 | Shell expansions, path issues |
| Naming | E301-E399 | Name collisions, invalid names |
| Validation | E401-E499 | Golden Format violations |
| SASMP | E501-E599 | Protocol compliance issues |
| Testing | E601-E699 | Test/build issues |
| Golden | E701-E704 | SKILL.md, assets, scripts, references |
| Mock | E801-E802 | Fake code detection |

## Output Example

```
DIAGNOSIS REPORT
================

Plugin: my-plugin
Symptom: "Agent not loading"

Root Cause Analysis:
--------------------

[E102] Malformed YAML Frontmatter
  Location: agents/my-agent.md:1
  Found: '>---'
  Expected: '---'
  Impact: Agent cannot be parsed
  Fix: Replace >--- with ---

[E103] Missing Required Fields
  Location: agents/my-agent.md
  Missing: 'model' field
  Impact: Agent cannot determine which model to use
  Fix: Add 'model: sonnet' to frontmatter

Proposed Fix Order:
1. Fix E102 (syntax) - Auto-fixable
2. Fix E103 (fields) - Auto-fixable

Estimated fix time: < 1 minute
```

## Quick Diagnosis Commands

```bash
# Check for E102 (malformed frontmatter)
grep -rl "^>---" agents/ skills/

# Check for E201 (shell expansions)
grep -rE '\$HOME|~/' --include="*.json" .

# Check for E303 (name collision)
jq -r '.name' .claude-plugin/plugin.json
jq -r '.name' .claude-plugin/marketplace.json
```

## Related Commands

- `/health-check` - Quick health score
- `/fix-golden-format` - Auto-fix Golden Format
- `/recover` - Recovery operations
