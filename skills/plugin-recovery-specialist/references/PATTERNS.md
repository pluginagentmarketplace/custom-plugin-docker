# Plugin Recovery Specialist Patterns

Design patterns and best practices for safe plugin recovery operations.

## Core Patterns

### Pattern 1: Backup-First

Always create backup before any modification:

```python
def safe_operation(plugin_path: Path, operation: Callable):
    """Execute operation with automatic backup"""
    # Create backup first
    backup_path = create_backup(plugin_path)

    try:
        # Execute operation
        result = operation(plugin_path)

        # Verify success
        if not verify_result(result):
            raise OperationError("Verification failed")

        return result

    except Exception as e:
        # Restore from backup
        restore_backup(backup_path, plugin_path)
        raise RecoveryError(f"Operation failed, restored backup: {e}")
```

### Pattern 2: Progressive Recovery

Try least invasive fix first:

```python
RECOVERY_LEVELS = [
    ("cache_clear", "low"),
    ("permission_fix", "low"),
    ("config_restore", "medium"),
    ("version_rollback", "high"),
]

def progressive_recovery(plugin_path: Path):
    """Try recovery actions in order of invasiveness"""
    for action, risk in RECOVERY_LEVELS:
        print(f"Trying {action} (risk: {risk})...")

        result = execute_action(plugin_path, action)

        if verify_health(plugin_path):
            return {"recovered": True, "action": action}

    return {"recovered": False, "tried": len(RECOVERY_LEVELS)}
```

### Pattern 3: Verification Loop

Always verify after recovery:

```python
def recover_and_verify(plugin_path: Path, action: str):
    """Execute recovery and verify result"""
    # Get initial health
    initial_health = get_health_score(plugin_path)

    # Execute recovery
    result = execute_action(plugin_path, action)

    if not result.success:
        return result

    # Verify improvement
    new_health = get_health_score(plugin_path)

    if new_health < initial_health:
        # Recovery made things worse, rollback
        rollback_last_action()
        return RecoveryResult(
            success=False,
            message="Recovery worsened health, rolled back"
        )

    return result
```

## Safety Patterns

### Safe File Operations

```python
def safe_write(path: Path, content: str):
    """Write file with backup"""
    # Backup existing
    if path.exists():
        backup = path.with_suffix(path.suffix + '.bak')
        shutil.copy2(path, backup)

    try:
        path.write_text(content)
    except Exception:
        # Restore backup
        if backup.exists():
            shutil.copy2(backup, path)
        raise
```

### Atomic Directory Operations

```python
def atomic_replace(source: Path, target: Path):
    """Atomically replace directory"""
    temp = target.with_name(target.name + '.tmp')

    # Copy to temp
    shutil.copytree(source, temp)

    # Backup current
    backup = target.with_name(target.name + '.bak')
    if target.exists():
        target.rename(backup)

    # Replace
    temp.rename(target)

    # Clean backup
    shutil.rmtree(backup, ignore_errors=True)
```

## Error Handling Patterns

### Graceful Degradation

```python
def recover_with_fallback(plugin_path: Path):
    """Try recovery with fallback options"""
    try:
        # Try primary recovery
        return primary_recovery(plugin_path)
    except RecoveryError:
        try:
            # Fallback to backup restore
            return restore_latest_backup(plugin_path)
        except BackupError:
            # Final fallback: reinstall
            return recommend_reinstall(plugin_path)
```

### Error Aggregation

```python
def batch_recovery(plugins: List[Path]):
    """Recover multiple plugins, collecting errors"""
    results = []
    errors = []

    for plugin in plugins:
        try:
            result = recover(plugin)
            results.append(result)
        except RecoveryError as e:
            errors.append({"plugin": plugin.name, "error": str(e)})

    return {
        "successful": len(results),
        "failed": len(errors),
        "errors": errors
    }
```

## Confirmation Patterns

### Interactive Confirmation

```python
def confirm_high_risk(action: str, details: str) -> bool:
    """Get user confirmation for high-risk action"""
    print("=" * 50)
    print("HIGH RISK ACTION CONFIRMATION")
    print("=" * 50)
    print(f"\nAction: {action}")
    print(f"Details: {details}")
    print("\nThis action cannot be easily undone.")
    print()

    response = input("Type 'yes' to confirm: ")
    return response.lower() == 'yes'
```

### CLI Flag Confirmation

```python
def check_confirmation(action_risk: str, args: List[str]) -> bool:
    """Check if action is confirmed via CLI"""
    if action_risk != "high":
        return True

    if "--confirm" in args:
        return True

    if "--dry-run" in args:
        print("DRY RUN: Would require --confirm for this action")
        return False

    print("This is a HIGH risk action.")
    print("Add --confirm to proceed.")
    return False
```

## Logging Patterns

### Recovery Audit Log

```python
def log_recovery_action(action: str, plugin: str, result: RecoveryResult):
    """Log recovery action for audit"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "plugin": plugin,
        "success": result.success,
        "message": result.message,
        "backup": result.backup_path
    }

    log_file = Path("/tmp/recovery-audit.log")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
```

## Testing Patterns

### Recovery Test Fixture

```python
@pytest.fixture
def broken_plugin(tmp_path):
    """Create a broken plugin for testing recovery"""
    plugin = tmp_path / "broken-plugin"
    plugin.mkdir()

    # Create structure with issues
    (plugin / ".claude-plugin").mkdir()
    (plugin / ".claude-plugin" / "plugin.json").write_text("invalid json")

    return plugin

def test_recovery_fixes_broken_plugin(broken_plugin):
    result = execute_action(broken_plugin, "config_restore")
    assert result.success
    assert get_health_score(broken_plugin) >= 85
```

## See Also

- [RECOVERY-GUIDE.md](RECOVERY-GUIDE.md)
- [SKILL.md](../SKILL.md)
- [Health Monitor Patterns](../../plugin-health-monitor/references/HEALTH-GUIDE.md)

---

Generated by plugin-health-agent
