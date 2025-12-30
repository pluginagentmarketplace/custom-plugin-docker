---
name: golden-format-validator
description: Comprehensive Golden Format compliance checking for E701-E704 errors with detailed reporting
sasmp_version: "1.3.0"
bonded_agent: plugin-health-agent
bond_type: SECONDARY_BOND
---

# Golden Format Validator Skill

Comprehensive Golden Format compliance checker detecting E701-E704 errors with detailed statistics and compliance reporting.

## Purpose

Detect all 4 Golden Format errors, validate SKILL.md size requirements, check subdirectory contents (not just existence), and distinguish real content from placeholders.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| plugin_path | string | Yes | - | Path to plugin directory |
| strict_mode | boolean | No | false | Fail on any violation |
| min_skill_size | number | No | 200 | Minimum SKILL.md bytes |
| min_asset_size | number | No | 100 | Minimum asset file bytes |
| report_format | enum | No | text | text/json/yaml |

## Golden Format Error Codes

### E701: Missing/Invalid SKILL.md

**Detection Criteria:**
- SKILL.md file missing entirely
- SKILL.md exists but < 200 bytes
- SKILL.md missing required YAML frontmatter

```bash
# Detection command
find "$SKILLS_DIR" -name "SKILL.md" -size -200c -exec echo "E701: {}" \;

# Check for missing SKILL.md
for dir in "$SKILLS_DIR"/*/; do
    if [ ! -f "${dir}SKILL.md" ]; then
        echo "E701: Missing SKILL.md in $dir"
    fi
done
```

**Expected Content:**
```markdown
---
name: skill-name
description: Skill purpose description
sasmp_version: "1.3.0"
bonded_agent: agent-name
bond_type: PRIMARY_BOND
---

# Skill Name

Detailed description of the skill...
(50+ lines with usage, examples, parameters)
```

### E702: Empty/Placeholder assets/ Directory

**Detection Criteria:**
- assets/ directory missing
- Contains only `.gitkeep`
- Contains only `README.md` with < 100 bytes

```bash
# Detection command
find "$SKILLS_DIR" -name "assets" -type d -exec sh -c '
    real_files=$(find "$1" -type f ! -name ".gitkeep" -size +100c | wc -l)
    if [ "$real_files" -eq 0 ]; then
        echo "E702: $1"
    fi
' _ {} \;
```

**Expected Content:**
- config.yaml or config.json (skill configuration)
- schema.json (input/output schema)
- templates/ (if applicable)
- examples/ (sample data)

### E703: Empty/Placeholder scripts/ Directory

**Detection Criteria:**
- scripts/ directory missing
- Contains only `.gitkeep`
- Contains only `README.md` with < 100 bytes

```bash
# Detection command
find "$SKILLS_DIR" -name "scripts" -type d -exec sh -c '
    real_files=$(find "$1" -type f ! -name ".gitkeep" -size +100c | wc -l)
    if [ "$real_files" -eq 0 ]; then
        echo "E703: $1"
    fi
' _ {} \;
```

**Expected Content:**
- validate.py or validate.sh (validation script)
- setup.sh (setup script)
- test_*.py (test files)
- utils.py (utility functions)

### E704: Empty/Placeholder references/ Directory

**Detection Criteria:**
- references/ directory missing
- Contains only `.gitkeep`
- Contains only `README.md` with < 100 bytes

```bash
# Detection command
find "$SKILLS_DIR" -name "references" -type d -exec sh -c '
    real_files=$(find "$1" -type f ! -name ".gitkeep" -size +100c | wc -l)
    if [ "$real_files" -eq 0 ]; then
        echo "E704: $1"
    fi
' _ {} \;
```

**Expected Content:**
- GUIDE.md (usage guide)
- PATTERNS.md (common patterns)
- API.md (API reference)
- EXAMPLES.md (examples)

## Comprehensive Validation Script

```python
#!/usr/bin/env python3
"""
golden_format_validator.py
Comprehensive Golden Format compliance checker
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Violation:
    error_code: str
    skill_name: str
    path: str
    issue: str
    auto_fixable: bool = True

def validate_skill_md(skill_path: Path) -> List[Violation]:
    """Validate SKILL.md file (E701)"""
    violations = []
    skill_name = skill_path.name
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        violations.append(Violation(
            "E701", skill_name, str(skill_md),
            "SKILL.md missing"
        ))
    elif skill_md.stat().st_size < 200:
        violations.append(Violation(
            "E701", skill_name, str(skill_md),
            f"SKILL.md too small ({skill_md.stat().st_size} bytes)"
        ))
    else:
        # Check YAML frontmatter
        content = skill_md.read_text()
        if not content.startswith("---"):
            violations.append(Violation(
                "E701", skill_name, str(skill_md),
                "Missing YAML frontmatter"
            ))

    return violations

def validate_subdirectory(skill_path: Path, subdir: str, error_code: str) -> List[Violation]:
    """Validate a skill subdirectory"""
    violations = []
    skill_name = skill_path.name
    subdir_path = skill_path / subdir

    if not subdir_path.exists():
        violations.append(Violation(
            error_code, skill_name, str(subdir_path),
            f"{subdir}/ directory missing"
        ))
        return violations

    # Get real files (not .gitkeep)
    real_files = [
        f for f in subdir_path.iterdir()
        if f.is_file() and f.name != ".gitkeep"
    ]

    if len(real_files) == 0:
        violations.append(Violation(
            error_code, skill_name, str(subdir_path),
            f"{subdir}/ contains only .gitkeep"
        ))
    elif len(real_files) == 1 and real_files[0].name.lower() == "readme.md":
        size = real_files[0].stat().st_size
        if size < 100:
            violations.append(Violation(
                error_code, skill_name, str(subdir_path),
                f"{subdir}/ contains only placeholder README ({size} bytes)"
            ))

    return violations

def validate_skill(skill_path: Path) -> List[Violation]:
    """Validate a single skill for Golden Format compliance"""
    violations = []

    # E701: SKILL.md
    violations.extend(validate_skill_md(skill_path))

    # E702: assets/
    violations.extend(validate_subdirectory(skill_path, "assets", "E702"))

    # E703: scripts/
    violations.extend(validate_subdirectory(skill_path, "scripts", "E703"))

    # E704: references/
    violations.extend(validate_subdirectory(skill_path, "references", "E704"))

    return violations

def validate_plugin(plugin_path: str) -> Tuple[List[Violation], dict]:
    """Validate all skills in a plugin"""
    skills_dir = Path(plugin_path) / "skills"
    all_violations = []
    stats = {
        "skills_checked": 0,
        "violations_by_code": {"E701": 0, "E702": 0, "E703": 0, "E704": 0}
    }

    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            stats["skills_checked"] += 1
            violations = validate_skill(skill_path)
            all_violations.extend(violations)

            for v in violations:
                stats["violations_by_code"][v.error_code] += 1

    return all_violations, stats

def main():
    if len(sys.argv) < 2:
        print("Usage: python golden_format_validator.py <plugin_path>")
        sys.exit(1)

    violations, stats = validate_plugin(sys.argv[1])

    print("=" * 60)
    print("GOLDEN FORMAT VALIDATION REPORT")
    print("=" * 60)
    print(f"\nSkills checked: {stats['skills_checked']}")
    print(f"Total violations: {len(violations)}")
    print(f"\nViolations by code:")
    for code, count in stats['violations_by_code'].items():
        print(f"  {code}: {count}")

    if violations:
        print(f"\n{'=' * 60}")
        print("VIOLATION DETAILS")
        print("=" * 60)
        for v in violations:
            print(f"\n[{v.error_code}] {v.skill_name}")
            print(f"  Path: {v.path}")
            print(f"  Issue: {v.issue}")
            print(f"  Auto-fixable: {'Yes' if v.auto_fixable else 'No'}")

        print(f"\n{'=' * 60}")
        print("RECOMMENDATION: Run golden-format-fixer to resolve violations")
        sys.exit(1)
    else:
        print(f"\n{'=' * 60}")
        print("STATUS: PASSED - All skills comply with Golden Format")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

## Validation Report

### Text Format

```
================================================================
GOLDEN FORMAT VALIDATION REPORT
================================================================
Plugin: my-plugin
Timestamp: 2025-12-30 15:30:00

SUMMARY
-------
Skills checked: 12
Total violations: 8

Violations by error code:
  E701 (Invalid SKILL.md):     2
  E702 (Empty assets/):        2
  E703 (Empty scripts/):       2
  E704 (Empty references/):    2

Compliance rate: 66.7% (4/12 skills clean)

================================================================
VIOLATION DETAILS
================================================================

[E701] api-client
  Path: skills/api-client/SKILL.md
  Issue: SKILL.md too small (95 bytes)
  Auto-fixable: Yes

[E702] database-connector
  Path: skills/database-connector/assets/
  Issue: Contains only placeholder README (45 bytes)
  Auto-fixable: Yes

[E703] auth-handler
  Path: skills/auth-handler/scripts/
  Issue: Contains only .gitkeep
  Auto-fixable: Yes

[E704] cache-manager
  Path: skills/cache-manager/references/
  Issue: Directory missing
  Auto-fixable: Yes

================================================================
RECOMMENDATION
================================================================
All violations are auto-fixable.
Run: golden-format-fixer --plugin my-plugin --fix-all
```

### JSON Format

```json
{
  "report_type": "golden_format_validation",
  "plugin": "my-plugin",
  "timestamp": "2025-12-30T15:30:00Z",
  "summary": {
    "skills_checked": 12,
    "total_violations": 8,
    "compliance_rate": 66.7,
    "violations_by_code": {
      "E701": 2,
      "E702": 2,
      "E703": 2,
      "E704": 2
    }
  },
  "violations": [
    {
      "error_code": "E701",
      "skill": "api-client",
      "path": "skills/api-client/SKILL.md",
      "issue": "SKILL.md too small (95 bytes)",
      "auto_fixable": true
    }
  ],
  "recommendation": "Run golden-format-fixer to resolve all violations"
}
```

## Batch Validation

```bash
#!/bin/bash
# batch-validate.sh
# Validate multiple plugins

PLUGINS_DIR="$1"
TOTAL=0
FAILED=0

for plugin in "$PLUGINS_DIR"/*/; do
    if [ -d "$plugin/.claude-plugin" ]; then
        echo "Validating: $(basename $plugin)"
        TOTAL=$((TOTAL + 1))

        if ! python golden_format_validator.py "$plugin" > /dev/null 2>&1; then
            FAILED=$((FAILED + 1))
            echo "  Status: FAILED"
        else
            echo "  Status: PASSED"
        fi
    fi
done

echo ""
echo "Summary: $((TOTAL - FAILED))/$TOTAL plugins passed"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `plugin_not_found` | Invalid path | Verify path exists |
| `skills_dir_missing` | No skills directory | Create skills/ directory |
| `encoding_error` | Non-UTF8 content | Fix file encoding |

## Usage

```
Skill("golden-format-validator")
```

## Assets

- `assets/golden-format-schema.json` - Golden Format specification
- `assets/validation-config.yaml` - Threshold settings
- `scripts/validate.py` - Python validation script
- `references/GOLDEN-FORMAT-GUIDE.md` - Format documentation

## Related Skills

- skill-subdirectory-validator (E401)
- golden-format-fixer (auto-repair)
- plugin-troubleshooter (other errors)
