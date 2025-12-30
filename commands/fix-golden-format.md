---
description: Auto-fix Golden Format violations (E701-E704) with category-aware content
allowed-tools: Read, Write, Bash, Glob, Grep, Edit
---

# /fix-golden-format Command

Automatically fix Golden Format violations (E701-E704) with intelligent, category-aware content generation.

## Usage

```
/fix-golden-format [plugin_path] [--skill skill_name] [--dry-run]
```

## What It Fixes

| Error | Issue | Fix Action |
|-------|-------|------------|
| E701 | Missing/small SKILL.md | Generate complete SKILL.md (50+ lines) |
| E702 | Placeholder assets/ | Add config.yaml + schema.json |
| E703 | Placeholder scripts/ | Add validate.py (131 lines) |
| E704 | Placeholder references/ | Add GUIDE.md + PATTERNS.md |

## Content Categories

The fixer auto-detects skill category for smart content:

| Category | Detected By | Assets | Scripts |
|----------|-------------|--------|---------|
| api | name contains api/rest/graphql | API config | API tests |
| testing | name contains test/spec | Test config | Test runners |
| devops | name contains deploy/ci/cd | Pipeline YAML | Deploy scripts |
| security | name contains auth/security | Security rules | Audit scripts |
| database | name contains db/sql | DB config | Migration scripts |
| frontend | name contains ui/react/vue | Component config | Build scripts |
| containers | name contains docker/k8s | Docker compose | Container checks |
| general | default | Generic config | Validation script |

## Example Output

```
GOLDEN FORMAT FIXER
===================
Plugin: my-plugin
Mode: Fix All

Processing: api-client
  [E701] Generating SKILL.md... DONE (52 lines)
  [E702] Adding assets/config.yaml... DONE
  [E702] Adding assets/schema.json... DONE
  [E703] Adding scripts/validate.py... DONE (131 lines)
  [E704] Adding references/GUIDE.md... DONE (95 lines)
  [E704] Adding references/PATTERNS.md... DONE (87 lines)

Processing: database-handler
  [E702] Adding assets/config.yaml... DONE
  [E703] Adding scripts/validate.py... DONE

Summary:
  Skills processed: 2
  Fixes applied: 7
  Success rate: 100%

Backup location: /tmp/golden-format-backup/...
```

## Dry Run Mode

Preview changes without applying:

```
/fix-golden-format . --dry-run

DRY RUN MODE
============
Would fix 7 violations in 2 skills:
  - api-client: E701, E702, E703, E704
  - database-handler: E702, E703

No changes made.
```

## Related Commands

- `/health-check` - Check current health
- `/diagnose` - Deep error diagnosis
- `/validate-structure` - Validate structure only
