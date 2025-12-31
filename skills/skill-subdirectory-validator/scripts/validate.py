#!/usr/bin/env python3
"""
Skill Subdirectory Validator Script
Version: 1.0.0

Detects E401 violations where skill subdirectories contain
only placeholder content (README.md < 100 bytes or .gitkeep only).
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

# Placeholder file patterns
PLACEHOLDER_FILES = {'.gitkeep', '.keep', '.placeholder'}
SMALL_README_THRESHOLD = 100  # bytes

@dataclass
class E401Violation:
    """Represents an E401 subdirectory violation"""
    skill_name: str
    subdirectory: str
    path: str
    reason: str
    file_count: int = 0
    total_size: int = 0

@dataclass
class ValidationReport:
    """Complete validation report"""
    plugin_name: str
    skills_checked: int = 0
    subdirs_checked: int = 0
    violations: List[E401Violation] = field(default_factory=list)

    @property
    def violation_count(self) -> int:
        return len(self.violations)

    @property
    def compliance_rate(self) -> float:
        if self.subdirs_checked == 0:
            return 100.0
        return (1 - self.violation_count / self.subdirs_checked) * 100

def is_placeholder_only(dir_path: Path) -> Tuple[bool, str, Dict]:
    """
    Check if directory contains only placeholder content.

    Returns: (is_placeholder, reason, stats)
    """
    if not dir_path.exists():
        return True, "directory_missing", {"files": 0, "size": 0}

    files = list(dir_path.iterdir())
    stats = {"files": 0, "size": 0}

    # Empty directory
    if len(files) == 0:
        return True, "empty", stats

    # Filter out placeholder files
    real_files = []
    for f in files:
        if f.is_file():
            if f.name not in PLACEHOLDER_FILES:
                real_files.append(f)
                stats["files"] += 1
                stats["size"] += f.stat().st_size

    # Only .gitkeep or similar
    if len(real_files) == 0:
        return True, "gitkeep_only", stats

    # Only small README.md
    if len(real_files) == 1:
        f = real_files[0]
        if f.name.lower() == 'readme.md':
            size = f.stat().st_size
            if size < SMALL_README_THRESHOLD:
                return True, f"small_readme ({size}b)", stats

    # Has real content
    return False, "has_content", stats

def validate_skill_subdirectories(skill_path: Path) -> List[E401Violation]:
    """Validate subdirectories of a single skill"""
    violations = []
    skill_name = skill_path.name

    for subdir_name in ['assets', 'scripts', 'references']:
        subdir_path = skill_path / subdir_name

        is_placeholder, reason, stats = is_placeholder_only(subdir_path)

        if is_placeholder:
            violations.append(E401Violation(
                skill_name=skill_name,
                subdirectory=subdir_name,
                path=str(subdir_path),
                reason=reason,
                file_count=stats["files"],
                total_size=stats["size"]
            ))

    return violations

def validate_plugin(plugin_path: str) -> ValidationReport:
    """Validate all skills in a plugin for E401 violations"""
    path = Path(plugin_path)
    skills_dir = path / 'skills'

    report = ValidationReport(plugin_name=path.name)

    if not skills_dir.exists():
        return report

    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            report.skills_checked += 1
            report.subdirs_checked += 3  # assets, scripts, references

            violations = validate_skill_subdirectories(skill_path)
            report.violations.extend(violations)

    return report

def print_report(report: ValidationReport, format: str = "text"):
    """Print validation report"""
    if format == "json":
        print(json.dumps({
            "plugin": report.plugin_name,
            "skills_checked": report.skills_checked,
            "subdirs_checked": report.subdirs_checked,
            "violations": report.violation_count,
            "compliance_rate": round(report.compliance_rate, 1),
            "details": [
                {
                    "skill": v.skill_name,
                    "subdir": v.subdirectory,
                    "path": v.path,
                    "reason": v.reason
                }
                for v in report.violations
            ]
        }, indent=2))
        return

    # Text format
    print("=" * 60)
    print("E401 SKILL SUBDIRECTORY VALIDATION")
    print("=" * 60)
    print(f"\nPlugin: {report.plugin_name}")
    print(f"Skills checked: {report.skills_checked}")
    print(f"Subdirectories checked: {report.subdirs_checked}")
    print(f"Violations found: {report.violation_count}")
    print(f"Compliance rate: {report.compliance_rate:.1f}%")

    if report.violations:
        print(f"\n{'-' * 60}")
        print("VIOLATIONS")
        print("-" * 60)

        # Group by skill
        by_skill: Dict[str, List[E401Violation]] = {}
        for v in report.violations:
            if v.skill_name not in by_skill:
                by_skill[v.skill_name] = []
            by_skill[v.skill_name].append(v)

        for skill_name, skill_violations in by_skill.items():
            print(f"\nSkill: {skill_name}")
            for v in skill_violations:
                print(f"  [E401] {v.subdirectory}/ - {v.reason}")

        print(f"\n{'-' * 60}")
        print("RECOMMENDATIONS")
        print("-" * 60)
        print("\nRun golden-format-fixer to add real content:")
        print("  python golden-format-fixer/scripts/fix.py /path/to/plugin")
    else:
        print(f"\n{'=' * 60}")
        print("STATUS: PASSED")
        print("All skill subdirectories have real content.")

    print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <plugin_path> [--json]")
        sys.exit(1)

    plugin_path = sys.argv[1]
    format = "json" if "--json" in sys.argv else "text"

    report = validate_plugin(plugin_path)
    print_report(report, format)

    sys.exit(0 if report.violation_count == 0 else 1)

if __name__ == "__main__":
    main()
