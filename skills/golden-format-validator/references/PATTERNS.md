# Golden Format Validator Patterns

Design patterns and best practices for Golden Format validation.

## Validation Patterns

### Pattern 1: Size-Based Detection

Detect placeholder files by size:

```python
def is_placeholder_readme(file_path: Path) -> bool:
    """README.md under 100 bytes is considered placeholder"""
    if file_path.name.lower() != 'readme.md':
        return False
    return file_path.stat().st_size < 100
```

### Pattern 2: Exclusion List

Filter out known placeholder files:

```python
PLACEHOLDER_FILES = {'.gitkeep', '.keep', '.placeholder'}

def get_real_files(directory: Path) -> List[Path]:
    """Get files excluding known placeholders"""
    return [
        f for f in directory.iterdir()
        if f.is_file() and f.name not in PLACEHOLDER_FILES
    ]
```

### Pattern 3: Progressive Validation

Validate in order of importance:

```python
def validate_skill(skill_path: Path) -> List[Violation]:
    violations = []

    # Critical: SKILL.md (E701)
    violations.extend(validate_skill_md(skill_path))

    # Important: Subdirectories (E702-E704)
    for subdir, code in [('assets', 'E702'), ('scripts', 'E703'), ('references', 'E704')]:
        violations.extend(validate_subdir(skill_path / subdir, code))

    return violations
```

## Detection Patterns

### Detecting Empty Directories

```python
def is_effectively_empty(dir_path: Path) -> bool:
    """Check if directory has no real content"""
    if not dir_path.exists():
        return True

    files = list(dir_path.iterdir())

    # Truly empty
    if not files:
        return True

    # Only .gitkeep
    real_files = [f for f in files if f.name != '.gitkeep']
    if not real_files:
        return True

    # Only small README
    if len(real_files) == 1:
        f = real_files[0]
        if f.name.lower() == 'readme.md' and f.stat().st_size < 100:
            return True

    return False
```

### Detecting Invalid Frontmatter

```python
def validate_frontmatter(content: str) -> Tuple[bool, List[str]]:
    """Validate YAML frontmatter in markdown"""
    errors = []

    if not content.startswith('---'):
        errors.append("Missing opening ---")
        return False, errors

    # Find closing ---
    second_marker = content.find('---', 3)
    if second_marker == -1:
        errors.append("Missing closing ---")
        return False, errors

    # Parse YAML
    try:
        frontmatter = yaml.safe_load(content[3:second_marker])
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML: {e}")
        return False, errors

    # Check required fields
    required = ['name', 'description', 'sasmp_version', 'bonded_agent', 'bond_type']
    for field in required:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")

    return len(errors) == 0, errors
```

## Reporting Patterns

### Structured Reports

```python
@dataclass
class ValidationReport:
    plugin_name: str
    skills_checked: int
    violations: List[Violation]

    def to_dict(self) -> Dict:
        return {
            "plugin": self.plugin_name,
            "skills": self.skills_checked,
            "violations": [v.to_dict() for v in self.violations],
            "compliance": self.compliance_rate
        }

    @property
    def compliance_rate(self) -> float:
        if self.skills_checked == 0:
            return 100.0
        max_violations = self.skills_checked * 4  # 4 checks per skill
        return (1 - len(self.violations) / max_violations) * 100
```

### Grouped Output

```python
def print_grouped_report(violations: List[Violation]):
    """Group violations by error code"""
    by_code = defaultdict(list)
    for v in violations:
        by_code[v.error_code].append(v)

    for code in sorted(by_code.keys()):
        print(f"\n{code}: {len(by_code[code])} violations")
        for v in by_code[code]:
            print(f"  - {v.skill_name}: {v.issue}")
```

## Anti-Patterns

### Anti-Pattern 1: Existence-Only Checks

```python
# BAD - Only checks existence
def bad_validate(skill_path):
    return (skill_path / 'assets').exists()

# GOOD - Checks content
def good_validate(skill_path):
    assets = skill_path / 'assets'
    if not assets.exists():
        return False
    return not is_effectively_empty(assets)
```

### Anti-Pattern 2: Ignoring Edge Cases

```python
# BAD - Doesn't handle .gitkeep
def bad_count_files(dir_path):
    return len(list(dir_path.iterdir()))

# GOOD - Excludes placeholders
def good_count_files(dir_path):
    return len([f for f in dir_path.iterdir()
                if f.name not in {'.gitkeep', '.keep'}])
```

## Testing Patterns

### Test Fixtures

```python
@pytest.fixture
def empty_skill(tmp_path):
    """Create skill with placeholder-only subdirs"""
    skill = tmp_path / "test-skill"
    skill.mkdir()

    (skill / "SKILL.md").write_text("---\nname: test\n---\n# Test")

    for subdir in ["assets", "scripts", "references"]:
        (skill / subdir).mkdir()
        (skill / subdir / ".gitkeep").touch()

    return skill

def test_detects_empty_assets(empty_skill):
    violations = validate_skill(empty_skill)
    codes = [v.error_code for v in violations]
    assert "E702" in codes
```

## See Also

- [GOLDEN-FORMAT-GUIDE.md](GOLDEN-FORMAT-GUIDE.md)
- [SKILL.md](../SKILL.md)
- [Fixer Patterns](../../golden-format-fixer/references/PATTERNS.md)

---

Generated by plugin-health-agent
