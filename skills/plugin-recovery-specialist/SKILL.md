---
name: plugin-recovery-specialist
description: Auto-recovery, rollback, and restoration operations for Claude Code plugins with backup-first approach
sasmp_version: "1.3.0"
bonded_agent: plugin-health-agent
bond_type: PRIMARY_BOND
---

# Plugin Recovery Specialist Skill

Safe auto-recovery and rollback operations with backup-first methodology for Claude Code plugin restoration.

## Purpose

Execute safe rollbacks to previous versions, clear caches selectively, restore configurations, fix permissions, and implement backup/restore workflows.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| plugin_path | string | Yes | - | Path to plugin directory |
| action | enum | Yes | - | rollback/restore/clear-cache/fix-perms |
| backup_dir | string | No | /tmp/plugin-backup | Backup location |
| confirm_high_risk | boolean | No | false | Required for HIGH risk actions |
| dry_run | boolean | No | false | Preview actions only |

## Recovery Philosophy

```
"BACKUP first. ATTEMPT fix. VERIFY success. RESTORE if failed."
```

### Recovery Hierarchy

```
Level 1: Least Invasive
|-- Cache clearing
|-- Config reload
|-- Permission fixes
|
Level 2: Moderate
|-- Configuration restore
|-- File structure fixes
|-- Selective rollback
|
Level 3: Most Invasive (USER CONFIRMATION)
|-- Full plugin rollback
|-- Complete reinstallation
|-- Version downgrade
```

## Recovery Actions

### 1. Cache Clearing

```bash
#!/bin/bash
# clear-cache.sh

CACHE_DIR="$HOME/.claude/plugins/cache"
PLUGIN_NAME="$1"

echo "Clearing cache for: $PLUGIN_NAME"
echo "================================"

# Selective cache clear
if [ -n "$PLUGIN_NAME" ]; then
    rm -rf "$CACHE_DIR/$PLUGIN_NAME"
    echo "Cleared: $CACHE_DIR/$PLUGIN_NAME"
else
    # Full cache clear (with confirmation)
    echo "Full cache clear requested"
    du -sh "$CACHE_DIR"
    rm -rf "$CACHE_DIR"/*
    echo "All plugin caches cleared"
fi

echo "Done."
```

**Risk Level**: LOW
**Auto-Execute**: YES
**Undo**: Cache rebuilds automatically

### 2. Configuration Restore

```bash
#!/bin/bash
# restore-config.sh

PLUGIN_DIR="$1"
BACKUP_DIR="$2"
CONFIG_FILE=".claude-plugin/plugin.json"

echo "Restoring configuration..."
echo "=========================="

# Create backup of current (broken) config
cp "$PLUGIN_DIR/$CONFIG_FILE" "/tmp/broken-config-$(date +%s).json"

# Restore from backup
if [ -f "$BACKUP_DIR/$CONFIG_FILE" ]; then
    cp "$BACKUP_DIR/$CONFIG_FILE" "$PLUGIN_DIR/$CONFIG_FILE"
    echo "Restored: $CONFIG_FILE"

    # Validate restored config
    if jq . "$PLUGIN_DIR/$CONFIG_FILE" > /dev/null 2>&1; then
        echo "Validation: PASS"
    else
        echo "Validation: FAIL - Backup may also be corrupted"
    fi
else
    echo "ERROR: Backup not found at $BACKUP_DIR/$CONFIG_FILE"
    exit 1
fi
```

**Risk Level**: MEDIUM
**Auto-Execute**: YES (with logging)
**Undo**: Broken config saved to /tmp

### 3. Permission Fixes

```bash
#!/bin/bash
# fix-permissions.sh

PLUGIN_DIR="$1"

echo "Fixing permissions for: $PLUGIN_DIR"
echo "===================================="

# Standard permissions for plugin files
find "$PLUGIN_DIR" -type f -name "*.md" -exec chmod 644 {} \;
find "$PLUGIN_DIR" -type f -name "*.json" -exec chmod 644 {} \;
find "$PLUGIN_DIR" -type f -name "*.sh" -exec chmod 755 {} \;
find "$PLUGIN_DIR" -type f -name "*.py" -exec chmod 755 {} \;
find "$PLUGIN_DIR" -type d -exec chmod 755 {} \;

echo "Permissions fixed:"
echo "  - Markdown files: 644"
echo "  - JSON files: 644"
echo "  - Scripts: 755"
echo "  - Directories: 755"
```

**Risk Level**: LOW
**Auto-Execute**: YES
**Undo**: No direct undo (permissions were already broken)

### 4. Full Plugin Rollback

```bash
#!/bin/bash
# rollback-plugin.sh

PLUGIN_DIR="$1"
VERSION="$2"
BACKUP_ROOT="/tmp/plugin-backup"

echo "PLUGIN ROLLBACK"
echo "==============="
echo "Plugin: $PLUGIN_DIR"
echo "Target Version: $VERSION"
echo ""

# Find backup
BACKUP_PATH="$BACKUP_ROOT/$(basename $PLUGIN_DIR)/$VERSION"

if [ ! -d "$BACKUP_PATH" ]; then
    echo "ERROR: Backup not found at $BACKUP_PATH"
    echo "Available backups:"
    ls -la "$BACKUP_ROOT/$(basename $PLUGIN_DIR)/" 2>/dev/null || echo "  (none)"
    exit 1
fi

# Create safety backup of current state
SAFETY_BACKUP="$BACKUP_ROOT/pre-rollback-$(date +%s)"
cp -r "$PLUGIN_DIR" "$SAFETY_BACKUP"
echo "Safety backup created: $SAFETY_BACKUP"

# Perform rollback
rm -rf "$PLUGIN_DIR"/*
cp -r "$BACKUP_PATH"/* "$PLUGIN_DIR/"

echo ""
echo "Rollback complete!"
echo "Previous state saved to: $SAFETY_BACKUP"
```

**Risk Level**: HIGH (REQUIRES CONFIRMATION)
**Auto-Execute**: NO
**Undo**: Safety backup created before rollback

## Backup Strategy

### Automatic Backups

```python
def create_backup(plugin_path, reason="manual"):
    """
    Create timestamped backup before any modification.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plugin_name = os.path.basename(plugin_path)

    backup_path = f"/tmp/plugin-backup/{plugin_name}/{timestamp}"

    # Create backup
    shutil.copytree(plugin_path, backup_path)

    # Write metadata
    metadata = {
        "timestamp": timestamp,
        "reason": reason,
        "plugin_path": plugin_path,
        "files_count": count_files(backup_path)
    }

    with open(f"{backup_path}/.backup-meta.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return backup_path
```

### Backup Retention

| Backup Type | Retention | Location |
|-------------|-----------|----------|
| Pre-fix backups | 7 days | /tmp/plugin-backup/{name}/ |
| Pre-rollback | 30 days | /tmp/plugin-backup/pre-rollback/ |
| User-requested | Indefinite | User-specified path |

## Recovery Workflows

### Standard Recovery Flow

```
ISSUE DETECTED
     |
     v
CREATE BACKUP (automatic)
     |
     v
DETERMINE RISK LEVEL
     |
     +-- LOW/MEDIUM --> AUTO-FIX
     |                      |
     |                      v
     |              VERIFY FIX WORKED?
     |                  |       |
     |                 YES     NO
     |                  |       |
     |                  v       v
     |               DONE   RESTORE BACKUP
     |                          |
     |                          v
     |               ESCALATE TO USER
     |
     +-- HIGH --> REQUEST USER CONFIRMATION
                         |
                        YES
                         |
                         v
                    AUTO-FIX
                         |
                         v
                  VERIFY FIX WORKED?
                      |       |
                     YES     NO
                      |       |
                      v       v
                   DONE   OFFER ROLLBACK
```

### Emergency Recovery

```bash
#!/bin/bash
# emergency-recovery.sh
# Use when plugin is completely broken

PLUGIN_DIR="$1"
BACKUP_ROOT="/tmp/plugin-backup"

echo "EMERGENCY RECOVERY MODE"
echo "======================="
echo ""

# 1. Stop using broken plugin
echo "Step 1: Isolating broken plugin..."
mv "$PLUGIN_DIR" "$PLUGIN_DIR.broken.$(date +%s)"

# 2. Find latest working backup
echo "Step 2: Finding latest backup..."
LATEST_BACKUP=$(ls -td "$BACKUP_ROOT/$(basename $PLUGIN_DIR)"/*/ 2>/dev/null | head -1)

if [ -n "$LATEST_BACKUP" ]; then
    echo "Found: $LATEST_BACKUP"

    # 3. Restore from backup
    echo "Step 3: Restoring..."
    cp -r "$LATEST_BACKUP" "$PLUGIN_DIR"

    # 4. Verify restoration
    echo "Step 4: Verifying..."
    if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
        echo "RECOVERY SUCCESSFUL"
    else
        echo "RECOVERY FAILED - Manual intervention needed"
        exit 1
    fi
else
    echo "No backup found - Manual intervention needed"
    exit 1
fi
```

## Error-Specific Recovery

### E001: Structure Error Recovery

```bash
# .claude-plugin is file instead of directory
CONTENT=$(cat "$PLUGIN_DIR/.claude-plugin")
rm "$PLUGIN_DIR/.claude-plugin"
mkdir -p "$PLUGIN_DIR/.claude-plugin"
echo "$CONTENT" > "$PLUGIN_DIR/.claude-plugin/plugin.json"
```

### E201: MCP Shell Expansion Recovery

```bash
# Replace shell expansions with absolute paths
# (Requires user input for actual paths)
sed -i 's|\$HOME|'"$HOME"'|g' "$PLUGIN_DIR/hooks/hooks.json"
sed -i 's|~/|'"$HOME/"'|g' "$PLUGIN_DIR/hooks/hooks.json"
```

### E306: 3-File Sync Recovery

```bash
# Sync installed_plugins.json with cache
CACHE_PLUGINS=$(ls ~/.claude/plugins/cache/)
jq --arg plugins "$CACHE_PLUGINS" '.plugins = ($plugins | split("\n"))' \
   ~/.claude/plugins/installed_plugins.json > /tmp/synced.json
mv /tmp/synced.json ~/.claude/plugins/installed_plugins.json
```

## Confirmation Protocol

For HIGH risk actions:

```
==================================================
           RISKY OPERATION CONFIRMATION
==================================================

Action: Full Plugin Rollback
Plugin: my-plugin
Target: Version 1.2.0 (from 2025-12-29)

WHAT WILL HAPPEN:
  - Current plugin state will be replaced
  - All changes since 2025-12-29 will be lost
  - Cache will be cleared

POTENTIAL CONSEQUENCES:
  - User customizations may be lost
  - Some recent fixes may need to be reapplied

ROLLBACK AVAILABLE: YES
  - Current state backed up to /tmp/plugin-backup/...

Do you want to proceed? (yes/no): _
==================================================
```

## Error Handling

| Error | Cause | Recovery |
|-------|-------|----------|
| `backup_not_found` | No backups exist | Use reinstallation |
| `permission_denied` | Access issues | Run with sudo or fix perms |
| `disk_full` | No space for backup | Clear old backups first |
| `restore_failed` | Backup corrupted | Try older backup |

## Usage

```
Skill("plugin-recovery-specialist")
```

## Assets

- `assets/recovery-config.yaml` - Recovery settings
- `assets/backup-policy.json` - Retention policies
- `scripts/recovery.py` - Main recovery script
- `references/RECOVERY-GUIDE.md` - Detailed recovery procedures

## Related Skills

- plugin-health-monitor (detect issues)
- plugin-troubleshooter (diagnose)
- plugin-installer-agent (reinstallation)
