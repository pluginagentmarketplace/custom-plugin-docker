---
description: Validate plugin structure and SASMP compliance
allowed-tools: Read, Bash, Glob, Grep
---

# /validate-structure Command

Validate plugin structure for Claude Code compatibility and SASMP v1.3.0 compliance.

## Usage

```
/validate-structure [plugin_path] [--strict]
```

## What It Validates

### Required Structure

```
plugin/
├── .claude-plugin/
│   └── plugin.json          [required]
├── agents/
│   └── *.md                  [at least 1]
├── skills/
│   └── skill-name/
│       ├── SKILL.md          [required]
│       ├── assets/           [required, with content]
│       ├── scripts/          [required, with content]
│       └── references/       [required, with content]
├── commands/
│   └── *.md                  [at least 1]
└── hooks/
    └── hooks.json            [optional]
```

### SASMP v1.3.0 Compliance

**Agent Requirements:**
- `name`: Agent identifier
- `description`: What the agent does
- `model`: sonnet/opus/haiku
- `tools`: List of allowed tools
- `sasmp_version`: "1.3.0"
- `eqhm_enabled`: true

**Skill Requirements:**
- `name`: Skill identifier
- `description`: What the skill does
- `sasmp_version`: "1.3.0"
- `bonded_agent`: Agent that owns this skill
- `bond_type`: PRIMARY_BOND or SECONDARY_BOND

**Command Requirements:**
- `description`: What the command does
- `allowed-tools`: Tools the command can use

## Output Example

```
STRUCTURE VALIDATION REPORT
===========================

Plugin: plugin-health-agent
SASMP Version: 1.3.0

Directory Structure:
  [OK] .claude-plugin/plugin.json
  [OK] agents/ (1 agent found)
  [OK] skills/ (6 skills found)
  [OK] commands/ (4 commands found)
  [OK] hooks/hooks.json

Agent Compliance:
  [OK] plugin-health-agent.md
    - name: plugin-health-agent
    - model: sonnet
    - sasmp_version: 1.3.0
    - eqhm_enabled: true

Skill Compliance:
  [OK] plugin-health-monitor
  [OK] plugin-troubleshooter
  [OK] plugin-recovery-specialist
  [OK] skill-subdirectory-validator
  [OK] golden-format-validator
  [OK] golden-format-fixer

Command Compliance:
  [OK] health-check.md
  [OK] diagnose.md
  [OK] fix-golden-format.md
  [OK] validate-structure.md

Golden Format (E701-E704):
  [OK] All skills have valid SKILL.md (> 200 bytes)
  [OK] All assets/ directories have real content
  [OK] All scripts/ directories have real content
  [OK] All references/ directories have real content

Result: PASSED (100% compliant)
```

## Strict Mode

Enable `--strict` for additional checks:

- No placeholder files allowed
- All optional fields must be present
- Documentation completeness
- Version consistency

## Related Commands

- `/health-check` - Full health analysis
- `/diagnose` - Error diagnosis
- `/fix-golden-format` - Auto-fix violations
