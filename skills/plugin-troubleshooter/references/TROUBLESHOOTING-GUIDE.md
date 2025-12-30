# Plugin Troubleshooting Guide

Comprehensive guide for diagnosing and resolving Claude Code plugin issues.

## Quick Diagnosis

### Agent Not Loading

1. Check YAML frontmatter exists:
   ```bash
   head -5 agents/my-agent.md
   ```

2. Check for E102 (malformed frontmatter):
   ```bash
   grep "^>---" agents/*.md
   ```

3. Verify required fields:
   - `name`
   - `description`
   - `model`
   - `tools`

### Skill Not Found

1. Check SKILL.md exists and size:
   ```bash
   ls -la skills/my-skill/SKILL.md
   ```

2. Check bonding in SKILL.md:
   - `bonded_agent`
   - `bond_type`

3. Verify in plugin.json:
   ```bash
   jq '.skills' .claude-plugin/plugin.json
   ```

### MCP Errors

1. Check for shell expansions:
   ```bash
   grep -rE '\$HOME|~/' --include="*.json" .
   ```

2. Convert to absolute paths:
   - `$HOME` -> `/home/user`
   - `~/` -> `/home/user/`

## Error Code Quick Reference

| Symptom | Check First | Error Codes |
|---------|-------------|-------------|
| Agent won't load | YAML frontmatter | E101, E102, E103 |
| Skill not found | SKILL.md exists | E701, E502 |
| Plugin not recognized | .claude-plugin/ | E001, E002, E003 |
| MCP fails | JSON configs | E201, E202 |
| Golden Format | Subdirectories | E401, E702-E704 |

## Common Fixes

### Fix E102 (Malformed Frontmatter)

```bash
# Replace >--- with ---
sed -i '1s/^>---/---/' agents/my-agent.md
```

### Fix E201 (Shell Expansion)

```bash
# Replace $HOME with actual path
sed -i "s|\$HOME|$HOME|g" hooks/hooks.json
```

### Fix E303 (Name Collision)

```bash
# Rename marketplace
jq '.name = "my-plugin-marketplace"' .claude-plugin/marketplace.json > tmp.json
mv tmp.json .claude-plugin/marketplace.json
```

### Fix E401/E701-E704 (Golden Format)

```bash
# Use golden-format-fixer
python scripts/fix.py /path/to/plugin --fix-all
```

## Diagnosis Commands

```bash
# Full diagnosis
python diagnose.py /path/to/plugin

# With symptom
python diagnose.py /path/to/plugin "agent not loading"

# JSON output
python diagnose.py /path/to/plugin --format json
```

## See Also

- [Error Codes Reference](../../../references/ERROR-CODES.md)
- [Health Monitoring Guide](../../plugin-health-monitor/references/HEALTH-GUIDE.md)
- [Recovery Procedures](../../plugin-recovery-specialist/references/RECOVERY-GUIDE.md)
