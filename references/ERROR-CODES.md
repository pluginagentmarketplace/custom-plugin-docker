# Plugin Health Agent - Error Codes Reference

Comprehensive reference for all 45+ error codes detected by the Plugin Health Agent.

---

## Error Code Summary

| Category | Code Range | Count | Auto-Fixable | Risk Levels |
|----------|------------|-------|--------------|-------------|
| Structural | E001-E099 | 10 | 8/10 | LOW-MEDIUM |
| Syntax | E101-E199 | 11 | 9/11 | LOW |
| Runtime | E201-E299 | 6 | 3/6 | HIGH |
| Naming | E301-E399 | 4 | 4/4 | LOW |
| Validation | E401-E499 | 10 | 8/10 | MEDIUM |
| SASMP Protocol | E501-E599 | 4 | 3/4 | LOW-MEDIUM |
| Testing | E601-E699 | 4 | 2/4 | MEDIUM-HIGH |
| Golden Format | E701-E704 | 4 | 4/4 | LOW |
| Mock Detection | E801-E802 | 2 | 0/2 | MEDIUM |

---

## Structural Errors (E001-E099)

### E001: .claude-plugin Structure Error

| Property | Value |
|----------|-------|
| **Detects** | `.claude-plugin` is FILE instead of DIRECTORY |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Backup file content > Delete file > Create directory > Restore as plugin.json |

**Detection:**
```bash
test -f .claude-plugin && echo "E001 detected"
```

**Fix:**
```bash
CONTENT=$(cat .claude-plugin)
rm .claude-plugin
mkdir -p .claude-plugin
echo "$CONTENT" > .claude-plugin/plugin.json
```

---

### E002: Missing plugin.json

| Property | Value |
|----------|-------|
| **Detects** | `.claude-plugin/plugin.json` file missing |
| **Auto-Fix** | YES (creates template) |
| **Risk Level** | LOW |
| **Action** | Generate minimal plugin.json with required fields |

---

### E003: Invalid plugin.json Schema

| Property | Value |
|----------|-------|
| **Detects** | Invalid JSON or missing required fields |
| **Auto-Fix** | PARTIAL |
| **Risk Level** | LOW |
| **Action** | Validate and add missing fields |

---

### E004-E007: Missing Required Directories

| Code | Missing Directory | Auto-Fix | Risk |
|------|------------------|----------|------|
| E004 | agents/ | YES | LOW |
| E005 | skills/ | YES | LOW |
| E006 | commands/ | YES | LOW |
| E007 | hooks/ | YES | LOW |

---

### E008: Incorrect File Permissions

| Property | Value |
|----------|-------|
| **Detects** | Files/directories with wrong permissions |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | `chmod 644` for files, `chmod 755` for directories/scripts |

---

### E009: Symlink Resolution Failure

| Property | Value |
|----------|-------|
| **Detects** | Broken symlinks in plugin structure |
| **Auto-Fix** | PARTIAL (removes broken links) |
| **Risk Level** | MEDIUM |

---

### E010: Path Traversal Vulnerability

| Property | Value |
|----------|-------|
| **Detects** | Path traversal attempts (../) in configurations |
| **Auto-Fix** | NO (security risk) |
| **Risk Level** | HIGH |
| **Action** | Manual review required |

---

## Syntax Errors (E101-E199)

### E101: Missing YAML Frontmatter

| Property | Value |
|----------|-------|
| **Detects** | Agent/skill file without YAML frontmatter |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Add required frontmatter block |

---

### E102: Malformed YAML Frontmatter

| Property | Value |
|----------|-------|
| **Detects** | YAML starts with `>---` instead of `---` |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Replace `>---` with `---` |

**Detection:**
```bash
grep -l "^>---" agents/*.md skills/*/SKILL.md
```

**Fix:**
```bash
sed -i '1s/^>---/---/' FILE
```

---

### E103: Missing Required YAML Fields

| Property | Value |
|----------|-------|
| **Detects** | Agent missing name, model, or tools fields |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |

**Required Agent Fields:**
- `name`
- `description`
- `model` (sonnet/opus/haiku)
- `tools`

**Required Skill Fields:**
- `name`
- `description`
- `sasmp_version`
- `bonded_agent`
- `bond_type`

---

### E104: Invalid YAML Syntax

| Property | Value |
|----------|-------|
| **Detects** | YAML parsing errors |
| **Auto-Fix** | PARTIAL |
| **Risk Level** | LOW |
| **Action** | Attempt common fixes (indentation, quotes) |

---

### E105: Invalid JSON in Config

| Property | Value |
|----------|-------|
| **Detects** | JSON parse errors in config files |
| **Auto-Fix** | YES (common fixes) |
| **Risk Level** | LOW |

---

### E106: Markdown Syntax Errors

| Property | Value |
|----------|-------|
| **Detects** | Malformed markdown structure |
| **Auto-Fix** | NO |
| **Risk Level** | LOW |

---

### E107-E111: Encoding/Whitespace Issues

| Code | Issue | Auto-Fix |
|------|-------|----------|
| E107 | Non-UTF8 encoding | YES |
| E108 | BOM character detected | YES |
| E109 | Trailing whitespace | YES |
| E110 | Inconsistent line endings | YES |
| E111 | Tab/space mixing | YES |

---

## Runtime Errors (E201-E299)

### E201: MCP Shell Expansion Bug

| Property | Value |
|----------|-------|
| **Detects** | Shell expansions in MCP config (`$HOME`, `~`, `$(...)`) |
| **Auto-Fix** | PARTIAL (needs absolute path info) |
| **Risk Level** | HIGH |
| **Action** | Identify problematic paths > Request user to provide absolute paths |

**Detection:**
```bash
grep -rE '\$\(|\$\{|\$HOME|~/' --include="*.json" .
```

**Common Patterns:**
- `$HOME/.local/bin` > `/home/user/.local/bin`
- `~/projects` > `/home/user/projects`
- `$(pwd)` > Actual absolute path

---

### E202: Environment Variable Missing

| Property | Value |
|----------|-------|
| **Detects** | Referenced env var not set |
| **Auto-Fix** | NO |
| **Risk Level** | MEDIUM |

---

### E203: Path Not Absolute

| Property | Value |
|----------|-------|
| **Detects** | Relative paths in configurations |
| **Auto-Fix** | YES (converts to absolute) |
| **Risk Level** | MEDIUM |

---

### E204: Binary Not Found

| Property | Value |
|----------|-------|
| **Detects** | Referenced executable not in PATH |
| **Auto-Fix** | NO |
| **Risk Level** | HIGH |

---

### E205: Permission Denied

| Property | Value |
|----------|-------|
| **Detects** | Access denied to required files |
| **Auto-Fix** | YES (chmod) |
| **Risk Level** | MEDIUM |

---

### E206: Resource Exhaustion

| Property | Value |
|----------|-------|
| **Detects** | Disk/memory limits reached |
| **Auto-Fix** | NO |
| **Risk Level** | HIGH |

---

## Naming Errors (E301-E399)

### E301: Invalid Plugin Name Characters

| Property | Value |
|----------|-------|
| **Detects** | Special characters in plugin name |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Valid Pattern** | `[a-z0-9-]+` |

---

### E302: Reserved Name Usage

| Property | Value |
|----------|-------|
| **Detects** | Using reserved names (claude, anthropic, etc.) |
| **Auto-Fix** | YES (adds prefix) |
| **Risk Level** | LOW |

---

### E303: Name Collision

| Property | Value |
|----------|-------|
| **Detects** | Marketplace name equals plugin name |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Rename marketplace to `{name}-marketplace` |

**Detection:**
```bash
PLUGIN=$(jq -r '.name' .claude-plugin/plugin.json)
MARKET=$(jq -r '.name' .claude-plugin/marketplace.json)
[ "$PLUGIN" = "$MARKET" ] && echo "E303"
```

---

### E304: Duplicate Agent Names

| Property | Value |
|----------|-------|
| **Detects** | Multiple agents with same name |
| **Auto-Fix** | YES (adds suffix) |
| **Risk Level** | LOW |

---

## Validation Errors (E401-E499)

### E401: Skill Subdirectory Violation

| Property | Value |
|----------|-------|
| **Detects** | assets/, scripts/, or references/ contains only README.md |
| **Auto-Fix** | YES (with templates) |
| **Risk Level** | MEDIUM |
| **Action** | Add real content files using category-specific templates |

**Detection:**
```bash
find skills -name "assets" -type d -exec sh -c \
  'count=$(find "$1" -type f ! -name ".gitkeep" -size +100c | wc -l);
   [ $count -eq 0 ] && echo "E401: $1"' _ {} \;
```

---

### E402-E410: Other Validation Errors

| Code | Issue | Auto-Fix | Risk |
|------|-------|----------|------|
| E402 | Missing required asset | YES | MEDIUM |
| E403 | Missing command frontmatter | YES | LOW |
| E404 | Invalid hook configuration | PARTIAL | MEDIUM |
| E405 | Circular skill dependency | NO | MEDIUM |
| E406 | Orphan file (not referenced) | NO | LOW |
| E407 | Version mismatch | YES | MEDIUM |
| E408 | Schema validation failure | PARTIAL | MEDIUM |
| E409 | Invalid bond type | YES | LOW |
| E410 | Missing bond reference | YES | LOW |

---

## SASMP Protocol Errors (E501-E599)

### E501: Missing SASMP Fields

| Property | Value |
|----------|-------|
| **Detects** | Agent missing `sasmp_version` or `eqhm_enabled` |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Add `sasmp_version: "1.3.0"` and `eqhm_enabled: true` |

---

### E502: Orphan Skill

| Property | Value |
|----------|-------|
| **Detects** | Skill without `bonded_agent` or `bond_type` |
| **Auto-Fix** | PARTIAL (needs agent info) |
| **Risk Level** | MEDIUM |

---

### E503: Ghost Agent

| Property | Value |
|----------|-------|
| **Detects** | Agent with no bonded skills |
| **Auto-Fix** | REQUIRES REVIEW |
| **Risk Level** | LOW |
| **Note** | May be intentional for standalone agents |

---

### E504: Missing Knowledge Graph

| Property | Value |
|----------|-------|
| **Detects** | Plugin without knowledge-graph.json + PNG |
| **Auto-Fix** | NO (complex generation) |
| **Risk Level** | LOW |

---

## Testing Errors (E601-E699)

### E601: venv Usage Detected

| Property | Value |
|----------|-------|
| **Detects** | venv/ directories or virtualenv usage |
| **Auto-Fix** | REQUIRES CONFIRMATION |
| **Risk Level** | HIGH (migration needed) |
| **Action** | Propose migration to UV package manager |

---

### E602: pip install Used

| Property | Value |
|----------|-------|
| **Detects** | Direct pip install commands in scripts/docs |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Replace with `uv pip install` |

---

### E603-E604: Build Issues

| Code | Issue | Auto-Fix | Risk |
|------|-------|----------|------|
| E603 | Build script errors | NO | MEDIUM |
| E604 | Test configuration issues | PARTIAL | MEDIUM |

---

## Golden Format Errors (E701-E704)

### E701: Missing/Invalid SKILL.md

| Property | Value |
|----------|-------|
| **Detects** | SKILL.md missing or < 200 bytes |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Generate complete SKILL.md with proper YAML frontmatter (50+ lines) |

---

### E702: Empty/Placeholder assets/ Directory

| Property | Value |
|----------|-------|
| **Detects** | Only .gitkeep OR tiny README.md (< 100 bytes) |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Add config.yaml + schema.json with real content |

---

### E703: Empty/Placeholder scripts/ Directory

| Property | Value |
|----------|-------|
| **Detects** | Only .gitkeep OR tiny README.md (< 100 bytes) |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Add validate.py (131 lines) with real validation logic |

---

### E704: Empty/Placeholder references/ Directory

| Property | Value |
|----------|-------|
| **Detects** | Only .gitkeep OR tiny README.md (< 100 bytes) |
| **Auto-Fix** | YES |
| **Risk Level** | LOW |
| **Action** | Add GUIDE.md (95 lines) + PATTERNS.md (87 lines) |

---

## Mock Detection Errors (E801-E802)

### E801: Mock Usage in Tests

| Property | Value |
|----------|-------|
| **Detects** | unittest.mock, MagicMock, @patch in test files |
| **Auto-Fix** | NO (requires real implementation) |
| **Risk Level** | MEDIUM |

---

### E802: Fake Test Scenarios

| Property | Value |
|----------|-------|
| **Detects** | Hardcoded return values in mock functions |
| **Auto-Fix** | NO (requires real test data) |
| **Risk Level** | MEDIUM |

---

## Quick Reference Commands

```bash
# Check all error types
python health-check.py /path/to/plugin --all-errors

# Check specific category
python health-check.py /path/to/plugin --category structural
python health-check.py /path/to/plugin --category golden-format

# Auto-fix safe errors
python health-check.py /path/to/plugin --auto-fix --risk-level medium

# Generate fix report
python health-check.py /path/to/plugin --output json > errors.json
```

---

## See Also

- [Health Monitoring Guide](../skills/plugin-health-monitor/references/HEALTH-GUIDE.md)
- [Recovery Procedures](../skills/plugin-recovery-specialist/references/RECOVERY-GUIDE.md)
- [Golden Format Guide](../skills/golden-format-validator/references/GOLDEN-FORMAT-GUIDE.md)
