#!/usr/bin/env python3
"""
Plugin Recovery Specialist Script
Version: 1.0.0

Safe auto-recovery and rollback operations with backup-first methodology.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class RecoveryAction:
    """Represents a recovery action"""
    name: str
    risk: str  # low, medium, high
    description: str
    reversible: bool = True

@dataclass
class RecoveryResult:
    """Result of a recovery action"""
    success: bool
    action: str
    message: str
    backup_path: Optional[str] = None

# Available recovery actions
ACTIONS = {
    "cache_clear": RecoveryAction(
        name="cache_clear",
        risk="low",
        description="Clear plugin cache"
    ),
    "permission_fix": RecoveryAction(
        name="permission_fix",
        risk="low",
        description="Fix file permissions"
    ),
    "config_restore": RecoveryAction(
        name="config_restore",
        risk="medium",
        description="Restore configuration from backup"
    ),
    "version_rollback": RecoveryAction(
        name="version_rollback",
        risk="high",
        description="Rollback to previous version"
    ),
    "backup_create": RecoveryAction(
        name="backup_create",
        risk="low",
        description="Create backup of current state"
    ),
    "backup_restore": RecoveryAction(
        name="backup_restore",
        risk="high",
        description="Restore from backup"
    )
}

def create_backup(plugin_path: Path, backup_dir: Path) -> str:
    """Create timestamped backup of plugin"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plugin_name = plugin_path.name
    backup_path = backup_dir / plugin_name / timestamp

    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(plugin_path, backup_path)

    # Write metadata
    metadata = {
        "timestamp": timestamp,
        "source": str(plugin_path),
        "files_count": sum(1 for _ in backup_path.rglob("*") if _.is_file())
    }
    (backup_path / ".backup-meta.json").write_text(json.dumps(metadata, indent=2))

    return str(backup_path)

def list_backups(plugin_name: str, backup_dir: Path) -> List[Dict]:
    """List available backups for a plugin"""
    backups = []
    plugin_backup_dir = backup_dir / plugin_name

    if not plugin_backup_dir.exists():
        return backups

    for backup_path in sorted(plugin_backup_dir.iterdir(), reverse=True):
        if backup_path.is_dir():
            meta_file = backup_path / ".backup-meta.json"
            if meta_file.exists():
                meta = json.loads(meta_file.read_text())
                backups.append({
                    "id": backup_path.name,
                    "path": str(backup_path),
                    **meta
                })

    return backups

def restore_backup(backup_path: Path, target_path: Path) -> bool:
    """Restore plugin from backup"""
    if not backup_path.exists():
        raise FileNotFoundError(f"Backup not found: {backup_path}")

    # Create safety backup of current state
    safety_backup = create_backup(target_path, Path("/tmp/plugin-backup/pre-restore"))

    try:
        # Remove current
        shutil.rmtree(target_path)

        # Restore from backup
        shutil.copytree(backup_path, target_path)

        # Remove backup metadata from restored
        meta_file = target_path / ".backup-meta.json"
        if meta_file.exists():
            meta_file.unlink()

        return True

    except Exception as e:
        # Restore from safety backup
        shutil.rmtree(target_path, ignore_errors=True)
        shutil.copytree(Path(safety_backup), target_path)
        raise RuntimeError(f"Restore failed, reverted to safety backup: {e}")

def fix_permissions(plugin_path: Path) -> Dict:
    """Fix file permissions"""
    fixed = {"files": 0, "directories": 0, "scripts": 0}

    for path in plugin_path.rglob("*"):
        if path.is_file():
            # Scripts get execute permission
            if path.suffix in [".sh", ".py"]:
                path.chmod(0o755)
                fixed["scripts"] += 1
            else:
                path.chmod(0o644)
                fixed["files"] += 1
        elif path.is_dir():
            path.chmod(0o755)
            fixed["directories"] += 1

    return fixed

def clear_cache(plugin_name: str) -> bool:
    """Clear plugin cache"""
    cache_dir = Path.home() / ".claude" / "plugins" / "cache" / plugin_name

    if cache_dir.exists():
        shutil.rmtree(cache_dir)
        return True
    return False

def execute_action(
    plugin_path: Path,
    action: str,
    backup_dir: Path = Path("/tmp/plugin-backup"),
    backup_id: Optional[str] = None,
    dry_run: bool = False
) -> RecoveryResult:
    """Execute a recovery action"""

    if action not in ACTIONS:
        return RecoveryResult(
            success=False,
            action=action,
            message=f"Unknown action: {action}"
        )

    action_info = ACTIONS[action]

    if dry_run:
        return RecoveryResult(
            success=True,
            action=action,
            message=f"DRY RUN: Would execute '{action_info.description}'"
        )

    try:
        if action == "cache_clear":
            success = clear_cache(plugin_path.name)
            return RecoveryResult(
                success=success,
                action=action,
                message="Cache cleared" if success else "No cache found"
            )

        elif action == "permission_fix":
            fixed = fix_permissions(plugin_path)
            return RecoveryResult(
                success=True,
                action=action,
                message=f"Fixed: {fixed['files']} files, {fixed['directories']} dirs, {fixed['scripts']} scripts"
            )

        elif action == "backup_create":
            backup_path = create_backup(plugin_path, backup_dir)
            return RecoveryResult(
                success=True,
                action=action,
                message=f"Backup created",
                backup_path=backup_path
            )

        elif action == "backup_restore":
            if not backup_id:
                return RecoveryResult(
                    success=False,
                    action=action,
                    message="backup_id required for restore"
                )

            backup_path = backup_dir / plugin_path.name / backup_id
            restore_backup(backup_path, plugin_path)
            return RecoveryResult(
                success=True,
                action=action,
                message=f"Restored from {backup_id}"
            )

        elif action == "version_rollback":
            backups = list_backups(plugin_path.name, backup_dir)
            if not backups:
                return RecoveryResult(
                    success=False,
                    action=action,
                    message="No backups available for rollback"
                )

            # Use most recent backup
            latest = backups[0]
            restore_backup(Path(latest["path"]), plugin_path)
            return RecoveryResult(
                success=True,
                action=action,
                message=f"Rolled back to {latest['id']}"
            )

        else:
            return RecoveryResult(
                success=False,
                action=action,
                message=f"Action not implemented: {action}"
            )

    except Exception as e:
        return RecoveryResult(
            success=False,
            action=action,
            message=f"Error: {str(e)}"
        )

def main():
    if len(sys.argv) < 3:
        print("Usage: python recovery.py <plugin_path> <action> [options]")
        print("\nActions:")
        for name, info in ACTIONS.items():
            print(f"  {name}: {info.description} (risk: {info.risk})")
        sys.exit(1)

    plugin_path = Path(sys.argv[1])
    action = sys.argv[2]
    dry_run = "--dry-run" in sys.argv
    backup_id = None

    for arg in sys.argv[3:]:
        if arg.startswith("--backup-id="):
            backup_id = arg.split("=")[1]

    if not plugin_path.exists():
        print(f"Error: Plugin not found: {plugin_path}")
        sys.exit(1)

    print("=" * 50)
    print("PLUGIN RECOVERY SPECIALIST")
    print("=" * 50)
    print(f"\nPlugin: {plugin_path}")
    print(f"Action: {action}")
    if dry_run:
        print("Mode: DRY RUN")
    print()

    # Check risk level
    if action in ACTIONS and ACTIONS[action].risk == "high":
        if "--confirm" not in sys.argv and not dry_run:
            print(f"WARNING: This is a HIGH risk action.")
            print("Add --confirm to proceed or --dry-run to preview.")
            sys.exit(1)

    result = execute_action(plugin_path, action, dry_run=dry_run, backup_id=backup_id)

    print(f"Result: {'SUCCESS' if result.success else 'FAILED'}")
    print(f"Message: {result.message}")
    if result.backup_path:
        print(f"Backup: {result.backup_path}")

    print("\n" + "=" * 50)

    sys.exit(0 if result.success else 1)

if __name__ == "__main__":
    main()
