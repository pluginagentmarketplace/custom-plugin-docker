# Skill Subdirectory Validation Guide

Comprehensive guide for detecting and fixing E401 subdirectory violations.

## What is E401?

E401 is an error code indicating that a skill's subdirectory (assets/, scripts/, or references/) contains only placeholder content instead of real files.

## Detection Criteria

A subdirectory is flagged as **E401 violation** if:

| Condition | Status |
|-----------|--------|
| Directory missing | E401 |
| Directory empty | E401 |
| Only `.gitkeep` | E401 |
| Only `README.md` < 100 bytes | E401 |
| Has real content files | OK |

## Required Structure

Each skill must have three subdirectories with real content:

```
skill-name/
├── SKILL.md              # Required
├── assets/               # E401 if placeholder-only
│   ├── config.yaml       # Real content
│   └── schema.json       # Real content
├── scripts/              # E401 if placeholder-only
│   └── validate.py       # Real content
└── references/           # E401 if placeholder-only
    ├── GUIDE.md          # Real content
    └── PATTERNS.md       # Real content
```

## Running Validation

### Command Line

```bash
# Validate all skills
python scripts/validate.py /path/to/plugin

# JSON output
python scripts/validate.py /path/to/plugin --json
```

### Sample Output

```
E401 SKILL SUBDIRECTORY VALIDATION
==================================

Plugin: my-plugin
Skills checked: 6
Subdirectories checked: 18
Violations found: 4
Compliance rate: 77.8%

------------------------------------------------------------
VIOLATIONS
------------------------------------------------------------

Skill: api-client
  [E401] assets/ - gitkeep_only
  [E401] scripts/ - empty

Skill: database
  [E401] references/ - small_readme (45b)
  [E401] assets/ - directory_missing

------------------------------------------------------------
RECOMMENDATIONS
------------------------------------------------------------

Run golden-format-fixer to add real content:
  python golden-format-fixer/scripts/fix.py /path/to/plugin
```

## Violation Types

### 1. directory_missing

The subdirectory doesn't exist at all.

```bash
# Check
ls skills/my-skill/assets/
# ls: cannot access 'skills/my-skill/assets/': No such file or directory
```

**Fix:**
```bash
mkdir -p skills/my-skill/assets
# Add real content files
```

### 2. empty

The subdirectory exists but is completely empty.

```bash
# Check
ls -la skills/my-skill/assets/
# total 0
```

**Fix:**
```bash
# Add real content files
touch skills/my-skill/assets/config.yaml
```

### 3. gitkeep_only

The subdirectory contains only `.gitkeep` placeholder.

```bash
# Check
ls -la skills/my-skill/assets/
# -rw-r--r-- 1 user user 0 Dec 30 12:00 .gitkeep
```

**Fix:**
```bash
# Add real content, then remove .gitkeep
echo "# Config" > skills/my-skill/assets/config.yaml
rm skills/my-skill/assets/.gitkeep
```

### 4. small_readme

The subdirectory only has a README.md under 100 bytes.

```bash
# Check
wc -c skills/my-skill/assets/README.md
# 45 skills/my-skill/assets/README.md
```

**Fix:**
```bash
# Add real content files alongside README
echo "# Config" > skills/my-skill/assets/config.yaml
```

## Fixing E401 Violations

### Automatic Fix

Use the golden-format-fixer:

```bash
python golden-format-fixer/scripts/fix.py /path/to/plugin
```

This will:
1. Detect all E401 violations
2. Generate category-appropriate content
3. Add real files to each subdirectory

### Manual Fix

For each subdirectory, add appropriate content:

#### assets/
```bash
# Create config.yaml
cat > skills/my-skill/assets/config.yaml << 'EOF'
skill:
  name: my-skill
  version: "1.0.0"

settings:
  enabled: true
EOF

# Create schema.json
echo '{"type": "object"}' > skills/my-skill/assets/schema.json
```

#### scripts/
```bash
# Create validate.py
cat > skills/my-skill/scripts/validate.py << 'EOF'
#!/usr/bin/env python3
"""Validation script for my-skill"""

def validate():
    print("Validation passed")

if __name__ == "__main__":
    validate()
EOF

chmod +x skills/my-skill/scripts/validate.py
```

#### references/
```bash
# Create GUIDE.md
echo "# Usage Guide\n\nDetailed usage documentation..." > skills/my-skill/references/GUIDE.md

# Create PATTERNS.md
echo "# Patterns\n\nBest practices..." > skills/my-skill/references/PATTERNS.md
```

## Best Practices

1. **Validate early** - Run validation before committing changes
2. **Use golden-format-fixer** - Automated fixing is faster and consistent
3. **Category-aware content** - Match content to skill purpose
4. **Remove placeholders** - Delete .gitkeep after adding real files

## Integration with CI/CD

```yaml
# GitHub Actions example
- name: Validate Skill Subdirectories
  run: |
    python skills/skill-subdirectory-validator/scripts/validate.py .
    if [ $? -ne 0 ]; then
      echo "E401 violations detected!"
      exit 1
    fi
```

## See Also

- [Golden Format Guide](../../golden-format-validator/references/GOLDEN-FORMAT-GUIDE.md)
- [Golden Format Fixer](../../golden-format-fixer/SKILL.md)
- [Error Codes Reference](../../../references/ERROR-CODES.md)

---

Generated by plugin-health-agent
