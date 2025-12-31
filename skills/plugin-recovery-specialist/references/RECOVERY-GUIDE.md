# Plugin Recovery Specialist Guide

Comprehensive guide for plugin recovery, rollback, and restoration operations.

## Overview

The Plugin Recovery Specialist provides safe recovery operations for Claude Code plugins using a backup-first methodology. All destructive operations create automatic backups.

## Recovery Philosophy

```
"BACKUP first. ATTEMPT fix. VERIFY success. RESTORE if failed."
```

## Available Actions

| Action | Risk | Description | Requires Confirmation |
|--------|------|-------------|----------------------|
| cache_clear | LOW | Clear plugin cache | No |
| permission_fix | LOW | Fix file permissions | No |
| config_restore | MEDIUM | Restore configuration | No |
| backup_create | LOW | Create backup | No |
| backup_restore | HIGH | Restore from backup | Yes |
| version_rollback | HIGH | Rollback to previous | Yes |

## Usage

### Command Line

```bash
# Clear cache (low risk)
python scripts/recovery.py /path/to/plugin cache_clear

# Fix permissions (low risk)
python scripts/recovery.py /path/to/plugin permission_fix

# Create backup (low risk)
python scripts/recovery.py /path/to/plugin backup_create

# Restore from backup (high risk - requires --confirm)
python scripts/recovery.py /path/to/plugin backup_restore --backup-id=20251230_143000 --confirm

# Dry run (preview only)
python scripts/recovery.py /path/to/plugin version_rollback --dry-run
```

### Programmatic

```python
from recovery import execute_action
from pathlib import Path

# Create backup
result = execute_action(
    plugin_path=Path("/home/user/my-plugin"),
    action="backup_create"
)

if result.success:
    print(f"Backup created: {result.backup_path}")
```

## Risk Levels

### LOW Risk (Auto-Execute)

- Cache clearing
- Permission fixes
- Backup creation
- Non-destructive operations

No confirmation required. Safe to run anytime.

### MEDIUM Risk (Auto with Logging)

- Configuration restore
- File structure fixes
- Selective rollback

Executes automatically but logs all changes for audit.

### HIGH Risk (Requires Confirmation)

- Full rollback
- Plugin reinstallation
- Bulk file deletion

Requires explicit `--confirm` flag or interactive confirmation.

## Backup System

### Automatic Backups

Backups are created automatically before:
- Any HIGH risk action
- Configuration changes
- Version updates

### Backup Location

```
/tmp/plugin-backup/
├── my-plugin/
│   ├── 20251230_140000/
│   │   ├── .backup-meta.json
│   │   ├── agents/
│   │   ├── skills/
│   │   └── ...
│   └── 20251230_150000/
│       └── ...
└── another-plugin/
    └── ...
```

### Backup Retention

| Type | Retention |
|------|-----------|
| Pre-action | 7 days |
| Pre-rollback | 30 days |
| User-created | Indefinite |

### Listing Backups

```bash
# List available backups
python scripts/recovery.py /path/to/plugin list_backups
```

Output:
```
Available backups for my-plugin:
  1. 20251230_150000 (latest)
     Created: 2025-12-30 15:00:00
     Files: 45
  2. 20251230_140000
     Created: 2025-12-30 14:00:00
     Files: 42
```

## Recovery Workflows

### Standard Recovery

```
1. Detect issue (via health check)
2. Create backup (automatic)
3. Attempt least invasive fix
4. Verify fix worked
5. If failed, try next level
6. If all fail, restore from backup
```

### Emergency Recovery

```
1. Isolate broken plugin (rename)
2. Find latest working backup
3. Restore from backup
4. Verify functionality
5. Investigate original issue
```

### Version Rollback

```
1. Create pre-rollback backup
2. Find target version backup
3. Restore target version
4. Verify plugin health
5. Re-apply safe customizations
```

## Common Recovery Scenarios

### Plugin Won't Load

1. Run permission fix:
   ```bash
   python scripts/recovery.py /path/to/plugin permission_fix
   ```

2. Clear cache:
   ```bash
   python scripts/recovery.py /path/to/plugin cache_clear
   ```

3. If still failing, check health:
   ```bash
   python health-check.py /path/to/plugin
   ```

### Configuration Corruption

1. Create backup of current state:
   ```bash
   python scripts/recovery.py /path/to/plugin backup_create
   ```

2. Restore from last working backup:
   ```bash
   python scripts/recovery.py /path/to/plugin backup_restore \
     --backup-id=20251230_140000 --confirm
   ```

### After Failed Update

1. Check available backups:
   ```bash
   python scripts/recovery.py /path/to/plugin list_backups
   ```

2. Rollback to pre-update:
   ```bash
   python scripts/recovery.py /path/to/plugin version_rollback --confirm
   ```

## Best Practices

1. **Always create backups** before major changes
2. **Test with --dry-run** before HIGH risk actions
3. **Verify after recovery** with health check
4. **Keep backup history** for at least 7 days
5. **Document customizations** for post-recovery reapplication

## Troubleshooting

### No Backups Available

If no backups exist:
1. Try permission fix and cache clear first
2. If still broken, reinstall from marketplace
3. Reapply customizations from documentation

### Restore Failed

If restore fails:
1. Check disk space
2. Verify backup integrity
3. Try older backup
4. Last resort: fresh install

### Permission Denied

If permission errors occur:
1. Run with appropriate permissions
2. Check file ownership
3. Verify directory permissions

## See Also

- [Plugin Health Monitor](../../plugin-health-monitor/SKILL.md)
- [Error Codes Reference](../../../references/ERROR-CODES.md)
- [Golden Format Guide](../../golden-format-validator/references/GOLDEN-FORMAT-GUIDE.md)

---

Generated by plugin-health-agent
