---
name: skill-subdirectory-validator
description: E401 violation detection - identifies README-only subdirectories in skills that violate Golden Format requirements
sasmp_version: "1.3.0"
bonded_agent: plugin-health-agent
bond_type: SECONDARY_BOND
---

# Skill Subdirectory Validator

Specialized detector for E401 violations where skill subdirectories (assets/, scripts/, references/) contain only placeholder content.

## Purpose

Scan all skills for empty or placeholder-only directories, detect Golden Format compliance violations, and generate detailed reports.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| plugin_path | string | Yes | - | Path to plugin directory |
| skills_dir | string | No | skills | Skills directory name |
| report_format | enum | No | text | text/json/yaml |
| include_suggestions | boolean | No | true | Include fix suggestions |

## E401: Skill Subdirectory Violation

### What It Detects

A skill subdirectory is considered **violated** if:

1. **Only .gitkeep**: Directory contains only `.gitkeep` file
2. **Placeholder README**: Contains only `README.md` with < 100 bytes
3. **Empty directory**: No files at all

### Required Structure (Golden Format)

```
skill/
├── SKILL.md           (required, > 200 bytes)
├── assets/            (required)
│   ├── README.md      (optional, for documentation)
│   └── config.yaml    (at least 1 REAL asset file)
├── scripts/           (required)
│   ├── README.md      (optional)
│   └── validate.py    (at least 1 REAL script)
└── references/        (required)
    ├── README.md      (optional)
    └── GUIDE.md       (at least 1 REAL reference doc)
```

### Detection Logic

```python
def is_placeholder_only(dir_path):
    """
    Detect if a directory contains only placeholder content.

    Returns: (is_placeholder: bool, reason: str)
    """
    if not os.path.isdir(dir_path):
        return True, "directory_missing"

    files = os.listdir(dir_path)

    # Empty directory
    if len(files) == 0:
        return True, "empty"

    # Only .gitkeep
    if files == ['.gitkeep']:
        return True, "gitkeep_only"

    # Filter out .gitkeep
    real_files = [f for f in files if f != '.gitkeep']

    # Only small README.md
    if len(real_files) == 1 and real_files[0].lower() == 'readme.md':
        readme_path = os.path.join(dir_path, real_files[0])
        if os.path.getsize(readme_path) < 100:
            return True, "small_readme"

    return False, "has_content"
```

## Validation Script

```bash
#!/bin/bash
# validate-subdirectories.sh
# Comprehensive E401 detector

PLUGIN_DIR="$1"
SKILLS_DIR="${PLUGIN_DIR}/skills"
VIOLATIONS=0
TOTAL_SUBDIRS=0

echo "=============================================="
echo "E401 SKILL SUBDIRECTORY VALIDATION"
echo "Plugin: $PLUGIN_DIR"
echo "=============================================="
echo ""

# Check each skill
for skill_dir in "$SKILLS_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    echo "Checking skill: $skill_name"

    for subdir in assets scripts references; do
        subdir_path="$skill_dir$subdir"
        TOTAL_SUBDIRS=$((TOTAL_SUBDIRS + 1))

        if [ ! -d "$subdir_path" ]; then
            echo "  [MISSING] $subdir/"
            VIOLATIONS=$((VIOLATIONS + 1))
            continue
        fi

        # Count files (excluding .gitkeep)
        file_count=$(find "$subdir_path" -type f ! -name ".gitkeep" | wc -l)

        # Check for small README only
        if [ "$file_count" -eq 1 ]; then
            readme_path="$subdir_path/README.md"
            if [ -f "$readme_path" ]; then
                size=$(stat -f%z "$readme_path" 2>/dev/null || stat -c%s "$readme_path" 2>/dev/null)
                if [ "$size" -lt 100 ]; then
                    echo "  [E401] $subdir/ (placeholder README only: ${size}b)"
                    VIOLATIONS=$((VIOLATIONS + 1))
                    continue
                fi
            fi
        fi

        if [ "$file_count" -eq 0 ]; then
            echo "  [E401] $subdir/ (empty or .gitkeep only)"
            VIOLATIONS=$((VIOLATIONS + 1))
        else
            echo "  [OK] $subdir/ ($file_count real files)"
        fi
    done
    echo ""
done

echo "=============================================="
echo "SUMMARY"
echo "=============================================="
echo "Total subdirectories checked: $TOTAL_SUBDIRS"
echo "Violations found: $VIOLATIONS"

if [ $VIOLATIONS -gt 0 ]; then
    echo ""
    echo "Status: FAILED"
    echo "Action: Run golden-format-fixer to add real content"
    exit 1
else
    echo ""
    echo "Status: PASSED"
    echo "All skill subdirectories have real content"
    exit 0
fi
```

## Detection Patterns

### Pattern 1: .gitkeep Only

```bash
# Detect directories with only .gitkeep
find "$SKILLS_DIR" -type d -name "assets" -exec sh -c '
    files=$(ls -A "$1" 2>/dev/null)
    if [ "$files" = ".gitkeep" ]; then
        echo "E401: $1 (gitkeep only)"
    fi
' _ {} \;
```

### Pattern 2: Tiny README Only

```bash
# Detect directories with README.md < 100 bytes as only real file
find "$SKILLS_DIR" -type d \( -name "assets" -o -name "scripts" -o -name "references" \) \
    -exec sh -c '
        real_files=$(find "$1" -type f ! -name ".gitkeep" | wc -l)
        if [ "$real_files" -eq 1 ]; then
            readme="$1/README.md"
            if [ -f "$readme" ]; then
                size=$(wc -c < "$readme")
                if [ "$size" -lt 100 ]; then
                    echo "E401: $1 (small README: ${size}b)"
                fi
            fi
        fi
    ' _ {} \;
```

### Pattern 3: Empty Directory

```bash
# Detect completely empty directories
find "$SKILLS_DIR" -type d -empty -name "assets" -o -empty -name "scripts" -o -empty -name "references"
```

## Validation Report Format

### Text Format

```
E401 VALIDATION REPORT
======================
Plugin: my-plugin
Timestamp: 2025-12-30 15:00:00

VIOLATIONS FOUND: 5

[E401] skills/api-client/assets/
  Status: PLACEHOLDER_ONLY
  Content: README.md (45 bytes)
  Expected: Real asset files (config.yaml, schema.json, etc.)
  Fix: golden-format-fixer --skill api-client --subdir assets

[E401] skills/api-client/scripts/
  Status: GITKEEP_ONLY
  Content: .gitkeep
  Expected: Real script files (validate.py, setup.sh, etc.)
  Fix: golden-format-fixer --skill api-client --subdir scripts

[E401] skills/database/references/
  Status: MISSING
  Content: Directory does not exist
  Expected: Reference documents (GUIDE.md, PATTERNS.md, etc.)
  Fix: golden-format-fixer --skill database --subdir references

SUMMARY
=======
Skills checked: 12
Subdirectories checked: 36
Violations: 5 (13.9%)
Compliance rate: 86.1%

RECOMMENDATION: Run golden-format-fixer to resolve all violations
```

### JSON Format

```json
{
  "report_type": "e401_validation",
  "plugin": "my-plugin",
  "timestamp": "2025-12-30T15:00:00Z",
  "summary": {
    "skills_checked": 12,
    "subdirectories_checked": 36,
    "violations": 5,
    "compliance_rate": 86.1
  },
  "violations": [
    {
      "error_code": "E401",
      "skill": "api-client",
      "subdirectory": "assets",
      "status": "PLACEHOLDER_ONLY",
      "content_found": "README.md (45 bytes)",
      "expected": "Real asset files",
      "auto_fixable": true,
      "fix_command": "golden-format-fixer --skill api-client --subdir assets"
    }
  ]
}
```

## Integration with Golden Format Fixer

```python
def validate_and_fix(plugin_path, auto_fix=False):
    """
    Validate skill subdirectories and optionally auto-fix violations.
    """
    violations = detect_e401_violations(plugin_path)

    if not violations:
        print("All subdirectories valid - no action needed")
        return True

    print(f"Found {len(violations)} E401 violations")

    if auto_fix:
        from golden_format_fixer import fix_violations
        fixed = fix_violations(violations)
        print(f"Fixed {fixed} of {len(violations)} violations")
        return fixed == len(violations)
    else:
        print("Run with auto_fix=True to repair violations")
        return False
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `skills_dir_not_found` | Invalid path | Verify plugin structure |
| `permission_denied` | Access issues | Check file permissions |
| `encoding_error` | Non-UTF8 files | Fix file encoding first |

## Usage

```
Skill("skill-subdirectory-validator")
```

## Assets

- `assets/validation-config.yaml` - Validation thresholds
- `assets/expected-structure.json` - Golden Format schema
- `scripts/validate-subdirs.py` - Python validator
- `references/VALIDATION-GUIDE.md` - Detailed validation docs

## Related Skills

- golden-format-validator (E701-E704)
- golden-format-fixer (auto-repair)
- plugin-troubleshooter (other errors)
