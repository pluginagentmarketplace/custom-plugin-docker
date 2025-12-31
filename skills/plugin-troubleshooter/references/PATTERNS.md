# Plugin Troubleshooter Patterns

Design patterns and best practices for deep diagnosis and root cause analysis.

## Core Patterns

### Pattern 1: Symptom-to-Code Mapping

Map user symptoms to error codes:

```python
SYMPTOM_MAP = {
    "agent not loading": ["E101", "E102", "E103", "E002"],
    "skill not found": ["E701", "E005", "E502"],
    "plugin not recognized": ["E001", "E002", "E003"],
    "yaml error": ["E102", "E103", "E104"],
    "json error": ["E003", "E105"],
    "mcp error": ["E201", "E202", "E203"],
    "permission denied": ["E008", "E205"],
    "golden format": ["E701", "E702", "E703", "E704"],
}

def map_symptom(symptom: str) -> List[str]:
    """Map symptom description to likely error codes"""
    symptom_lower = symptom.lower()
    codes = []

    for key, error_codes in SYMPTOM_MAP.items():
        if key in symptom_lower:
            codes.extend(error_codes)

    return list(set(codes))  # Remove duplicates
```

### Pattern 2: Progressive Diagnosis

Start with quick checks, go deeper if needed:

```python
def progressive_diagnosis(plugin_path: Path):
    """Diagnose progressively from quick to deep"""

    # Level 1: Quick structure check
    issues = check_structure(plugin_path)
    if issues:
        return {"level": 1, "issues": issues}

    # Level 2: Syntax validation
    issues = check_syntax(plugin_path)
    if issues:
        return {"level": 2, "issues": issues}

    # Level 3: Deep content analysis
    issues = deep_analysis(plugin_path)
    if issues:
        return {"level": 3, "issues": issues}

    return {"level": 0, "issues": [], "status": "healthy"}
```

### Pattern 3: Root Cause Analysis

Trace errors to their root cause:

```python
def find_root_cause(error_code: str, context: Dict) -> str:
    """Determine root cause from error and context"""

    ROOT_CAUSES = {
        "E102": {
            "pattern": ">---",
            "cause": "File was created with incorrect frontmatter delimiter",
            "likely_source": "Copy-paste error or template issue"
        },
        "E201": {
            "pattern": "$HOME",
            "cause": "MCP cannot expand shell variables at runtime",
            "likely_source": "Configuration copied from shell script"
        },
        "E303": {
            "pattern": "name collision",
            "cause": "Plugin and marketplace have identical names",
            "likely_source": "Marketplace created from plugin template without renaming"
        }
    }

    if error_code in ROOT_CAUSES:
        return ROOT_CAUSES[error_code]

    return {"cause": "Unknown", "likely_source": "Requires manual investigation"}
```

## Detection Patterns

### File Content Analysis

```python
def analyze_file_content(file_path: Path) -> List[Issue]:
    """Analyze file content for common issues"""
    issues = []
    content = file_path.read_text()

    # Check frontmatter
    if file_path.suffix == '.md':
        if content.startswith('>---'):
            issues.append(Issue("E102", "Malformed frontmatter"))
        elif not content.startswith('---'):
            issues.append(Issue("E101", "Missing frontmatter"))

    # Check for shell expansions in JSON
    if file_path.suffix == '.json':
        shell_patterns = ['$HOME', '$USER', '~/', '$(', '${']
        for pattern in shell_patterns:
            if pattern in content:
                issues.append(Issue("E201", f"Shell expansion: {pattern}"))

    return issues
```

### Directory Structure Analysis

```python
def analyze_structure(plugin_path: Path) -> List[Issue]:
    """Analyze plugin directory structure"""
    issues = []

    required = {
        '.claude-plugin': 'E001',
        '.claude-plugin/plugin.json': 'E002',
        'agents': 'E004',
        'skills': 'E005',
        'commands': 'E006',
        'hooks': 'E007'
    }

    for path, error_code in required.items():
        full_path = plugin_path / path
        if not full_path.exists():
            issues.append(Issue(error_code, f"Missing: {path}"))

    return issues
```

## Reporting Patterns

### Structured Diagnosis Report

```python
@dataclass
class DiagnosisReport:
    plugin: str
    symptom: Optional[str]
    issues: List[Issue]
    root_causes: List[str]
    recommendations: List[str]

    def to_dict(self) -> Dict:
        return {
            "plugin": self.plugin,
            "symptom": self.symptom,
            "issues_count": len(self.issues),
            "issues": [i.to_dict() for i in self.issues],
            "root_causes": self.root_causes,
            "recommendations": self.recommendations
        }
```

### Priority-Ordered Output

```python
def prioritize_issues(issues: List[Issue]) -> List[Issue]:
    """Sort issues by severity and fixability"""
    priority_order = {
        "HIGH": 0,
        "MEDIUM": 1,
        "LOW": 2
    }

    return sorted(issues, key=lambda i: (
        priority_order.get(i.severity, 99),
        0 if i.auto_fixable else 1
    ))
```

## Anti-Patterns

### Anti-Pattern 1: Blind Guessing

```python
# BAD - Guessing without evidence
def bad_diagnose(symptom):
    return "Try reinstalling the plugin"

# GOOD - Evidence-based diagnosis
def good_diagnose(plugin_path, symptom):
    # Collect evidence
    evidence = scan_for_issues(plugin_path)

    # Map to error codes
    codes = map_symptom_to_codes(symptom, evidence)

    # Return specific diagnosis
    return {
        "codes": codes,
        "evidence": evidence,
        "recommendations": get_fixes(codes)
    }
```

### Anti-Pattern 2: Single-Point Failure

```python
# BAD - Stops at first error
def bad_scan(plugin_path):
    if not check_structure(plugin_path):
        return "Structure error"
    # Never checks anything else

# GOOD - Complete scan
def good_scan(plugin_path):
    all_issues = []
    all_issues.extend(check_structure(plugin_path))
    all_issues.extend(check_syntax(plugin_path))
    all_issues.extend(check_content(plugin_path))
    return all_issues  # Complete picture
```

## Workflow Patterns

### Diagnosis Workflow

```
1. Receive symptom/request
2. Quick structure scan
3. Map symptom to likely codes
4. Deep scan for those codes
5. Find root causes
6. Generate recommendations
7. Return prioritized report
```

### Iterative Refinement

```python
def iterative_diagnosis(plugin_path: Path, max_iterations: int = 3):
    """Refine diagnosis through iterations"""
    all_issues = []

    for i in range(max_iterations):
        # Scan
        new_issues = scan(plugin_path, exclude=all_issues)

        if not new_issues:
            break

        all_issues.extend(new_issues)

        # Try to fix auto-fixable issues
        fixed = auto_fix([i for i in new_issues if i.auto_fixable])

        if not fixed:
            break  # No progress possible

    return all_issues
```

## See Also

- [TROUBLESHOOTING-GUIDE.md](TROUBLESHOOTING-GUIDE.md)
- [SKILL.md](../SKILL.md)
- [Error Codes Reference](../../../references/ERROR-CODES.md)

---

Generated by plugin-health-agent
