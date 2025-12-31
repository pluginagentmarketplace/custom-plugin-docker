# Skill Subdirectory Validator Patterns

Design patterns for E401 detection and subdirectory validation.

## Detection Patterns

### Pattern 1: Multi-Level Check

Check multiple conditions in order:

```python
def is_placeholder_only(dir_path: Path) -> Tuple[bool, str]:
    """
    Check directory for placeholder-only content.
    Returns (is_placeholder, reason)
    """
    # Level 1: Existence
    if not dir_path.exists():
        return True, "missing"

    files = list(dir_path.iterdir())

    # Level 2: Empty
    if len(files) == 0:
        return True, "empty"

    # Level 3: Placeholder files only
    real_files = [f for f in files if f.name not in PLACEHOLDER_FILES]
    if len(real_files) == 0:
        return True, "placeholder_only"

    # Level 4: Small README only
    if len(real_files) == 1:
        f = real_files[0]
        if f.name.lower() == 'readme.md' and f.stat().st_size < 100:
            return True, "small_readme"

    # Has real content
    return False, "valid"
```

### Pattern 2: Configurable Thresholds

Use configuration for validation rules:

```python
class ValidationConfig:
    placeholder_files = {'.gitkeep', '.keep'}
    small_file_threshold = 100  # bytes
    required_subdirs = ['assets', 'scripts', 'references']

def validate_with_config(dir_path: Path, config: ValidationConfig) -> bool:
    """Validate using configurable rules"""
    files = [f for f in dir_path.iterdir()
             if f.name not in config.placeholder_files]

    if len(files) == 0:
        return False

    # Check if all files are too small
    real_files = [f for f in files
                  if f.stat().st_size >= config.small_file_threshold]

    return len(real_files) > 0
```

### Pattern 3: Detailed Statistics

Collect detailed information during validation:

```python
@dataclass
class SubdirStats:
    exists: bool
    file_count: int
    total_size: int
    placeholder_count: int
    real_file_count: int

def analyze_subdirectory(dir_path: Path) -> SubdirStats:
    """Get detailed statistics about subdirectory"""
    if not dir_path.exists():
        return SubdirStats(False, 0, 0, 0, 0)

    files = list(dir_path.iterdir())
    placeholders = [f for f in files if f.name in PLACEHOLDER_FILES]
    real_files = [f for f in files if f not in placeholders]
    total_size = sum(f.stat().st_size for f in files if f.is_file())

    return SubdirStats(
        exists=True,
        file_count=len(files),
        total_size=total_size,
        placeholder_count=len(placeholders),
        real_file_count=len(real_files)
    )
```

## Reporting Patterns

### Grouped Report

```python
def generate_grouped_report(violations: List[E401Violation]) -> str:
    """Generate report grouped by skill"""
    by_skill = {}
    for v in violations:
        if v.skill_name not in by_skill:
            by_skill[v.skill_name] = []
        by_skill[v.skill_name].append(v)

    lines = []
    for skill, skill_violations in sorted(by_skill.items()):
        lines.append(f"\n{skill}:")
        for v in skill_violations:
            lines.append(f"  [{v.subdirectory}] {v.reason}")

    return "\n".join(lines)
```

### Summary Statistics

```python
def generate_summary(report: ValidationReport) -> Dict:
    """Generate summary statistics"""
    by_reason = {}
    by_subdir = {'assets': 0, 'scripts': 0, 'references': 0}

    for v in report.violations:
        by_reason[v.reason] = by_reason.get(v.reason, 0) + 1
        by_subdir[v.subdirectory] += 1

    return {
        "total_skills": report.skills_checked,
        "total_violations": report.violation_count,
        "by_reason": by_reason,
        "by_subdirectory": by_subdir,
        "compliance_rate": report.compliance_rate
    }
```

## Validation Patterns

### Batch Validation

```python
def validate_all_skills(plugin_path: Path) -> List[E401Violation]:
    """Validate all skills in plugin"""
    violations = []
    skills_dir = plugin_path / 'skills'

    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            skill_violations = validate_skill(skill_path)
            violations.extend(skill_violations)

    return violations
```

### Selective Validation

```python
def validate_specific_subdirs(
    skill_path: Path,
    subdirs: List[str]
) -> List[E401Violation]:
    """Validate only specific subdirectories"""
    violations = []

    for subdir in subdirs:
        if subdir not in ['assets', 'scripts', 'references']:
            continue

        subdir_path = skill_path / subdir
        is_placeholder, reason, _ = is_placeholder_only(subdir_path)

        if is_placeholder:
            violations.append(E401Violation(
                skill_name=skill_path.name,
                subdirectory=subdir,
                path=str(subdir_path),
                reason=reason
            ))

    return violations
```

## Anti-Patterns

### Anti-Pattern 1: Existence-Only Check

```python
# BAD - Only checks if directory exists
def bad_validate(skill_path):
    return (skill_path / 'assets').exists()

# GOOD - Checks for real content
def good_validate(skill_path):
    assets = skill_path / 'assets'
    if not assets.exists():
        return False
    return not is_placeholder_only(assets)[0]
```

### Anti-Pattern 2: Ignoring File Size

```python
# BAD - Counts any file as valid
def bad_count(dir_path):
    return len([f for f in dir_path.iterdir() if f.is_file()])

# GOOD - Excludes small placeholders
def good_count(dir_path):
    return len([f for f in dir_path.iterdir()
                if f.is_file()
                and f.name not in PLACEHOLDER_FILES
                and f.stat().st_size >= 100])
```

## Testing Patterns

### Test Fixtures

```python
@pytest.fixture
def placeholder_skill(tmp_path):
    """Create skill with placeholder-only subdirs"""
    skill = tmp_path / "test-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("# Test\n" * 50)

    for subdir in ["assets", "scripts", "references"]:
        (skill / subdir).mkdir()
        (skill / subdir / ".gitkeep").touch()

    return skill

def test_detects_placeholder(placeholder_skill):
    violations = validate_skill_subdirectories(placeholder_skill)
    assert len(violations) == 3
    assert all(v.subdirectory in ['assets', 'scripts', 'references']
               for v in violations)
```

## See Also

- [VALIDATION-GUIDE.md](VALIDATION-GUIDE.md)
- [SKILL.md](../SKILL.md)
- [Golden Format Patterns](../../golden-format-validator/references/PATTERNS.md)

---

Generated by plugin-health-agent
