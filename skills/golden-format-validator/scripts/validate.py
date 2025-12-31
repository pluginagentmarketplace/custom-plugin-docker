#!/usr/bin/env python3
"""
Golden Format Validator Script
Version: 1.0.0

Validates Claude Code plugin skills for Golden Format compliance.
Detects E701-E704 violations with detailed reporting.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class Violation:
    """Represents a Golden Format violation"""
    error_code: str
    skill_name: str
    path: str
    issue: str
    suggestion: str
    auto_fixable: bool = True

@dataclass
class ValidationReport:
    """Complete validation report"""
    plugin_name: str
    skills_checked: int = 0
    violations: List[Violation] = field(default_factory=list)

    @property
    def total_violations(self) -> int:
        return len(self.violations)

    @property
    def compliance_rate(self) -> float:
        if self.skills_checked == 0:
            return 100.0
        violations_per_skill = self.total_violations / (self.skills_checked * 4)  # 4 checks per skill
        return max(0, (1 - violations_per_skill) * 100)

    @property
    def by_error_code(self) -> Dict[str, int]:
        counts = {"E701": 0, "E702": 0, "E703": 0, "E704": 0}
        for v in self.violations:
            counts[v.error_code] += 1
        return counts

def is_placeholder_only(dir_path: Path) -> Tuple[bool, str]:
    """
    Check if directory contains only placeholder content.

    Returns: (is_placeholder, reason)
    """
    if not dir_path.exists():
        return True, "missing"

    files = list(dir_path.iterdir())

    # Empty directory
    if len(files) == 0:
        return True, "empty"

    # Only .gitkeep
    file_names = [f.name for f in files]
    if file_names == ['.gitkeep']:
        return True, "gitkeep_only"

    # Filter out .gitkeep
    real_files = [f for f in files if f.name != '.gitkeep' and f.is_file()]

    # Only small README.md
    if len(real_files) == 1 and real_files[0].name.lower() == 'readme.md':
        size = real_files[0].stat().st_size
        if size < 100:
            return True, f"small_readme ({size}b)"

    # Has real content
    return False, "has_content"

def validate_skill_md(skill_path: Path) -> List[Violation]:
    """Validate SKILL.md (E701)"""
    violations = []
    skill_name = skill_path.name
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        violations.append(Violation(
            error_code="E701",
            skill_name=skill_name,
            path=str(skill_md),
            issue="SKILL.md file missing",
            suggestion="Generate SKILL.md with proper YAML frontmatter"
        ))
    elif skill_md.stat().st_size < 200:
        violations.append(Violation(
            error_code="E701",
            skill_name=skill_name,
            path=str(skill_md),
            issue=f"SKILL.md too small ({skill_md.stat().st_size} bytes)",
            suggestion="Expand SKILL.md to at least 200 bytes with documentation"
        ))
    else:
        # Check frontmatter
        content = skill_md.read_text()
        if not content.startswith('---'):
            violations.append(Violation(
                error_code="E701",
                skill_name=skill_name,
                path=str(skill_md),
                issue="SKILL.md missing YAML frontmatter",
                suggestion="Add YAML frontmatter with required fields"
            ))

    return violations

def validate_subdirectory(skill_path: Path, subdir: str, error_code: str) -> List[Violation]:
    """Validate a skill subdirectory (E702/E703/E704)"""
    violations = []
    skill_name = skill_path.name
    subdir_path = skill_path / subdir

    is_placeholder, reason = is_placeholder_only(subdir_path)

    if is_placeholder:
        violations.append(Violation(
            error_code=error_code,
            skill_name=skill_name,
            path=str(subdir_path),
            issue=f"{subdir}/ is {reason}",
            suggestion=f"Add real content files to {subdir}/"
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

def validate_plugin(plugin_path: str) -> ValidationReport:
    """Validate all skills in a plugin"""
    path = Path(plugin_path)
    skills_dir = path / 'skills'

    report = ValidationReport(plugin_name=path.name)

    if not skills_dir.exists():
        return report

    for skill_path in skills_dir.iterdir():
        if skill_path.is_dir():
            report.skills_checked += 1
            violations = validate_skill(skill_path)
            report.violations.extend(violations)

    return report

def print_report(report: ValidationReport, format: str = "text"):
    """Print validation report"""
    if format == "json":
        print(json.dumps({
            "plugin": report.plugin_name,
            "skills_checked": report.skills_checked,
            "total_violations": report.total_violations,
            "compliance_rate": round(report.compliance_rate, 1),
            "by_code": report.by_error_code,
            "violations": [
                {
                    "code": v.error_code,
                    "skill": v.skill_name,
                    "path": v.path,
                    "issue": v.issue,
                    "suggestion": v.suggestion
                }
                for v in report.violations
            ]
        }, indent=2))
        return

    # Text format
    print("=" * 60)
    print("GOLDEN FORMAT VALIDATION REPORT")
    print("=" * 60)
    print(f"\nPlugin: {report.plugin_name}")
    print(f"Skills checked: {report.skills_checked}")
    print(f"Total violations: {report.total_violations}")
    print(f"Compliance rate: {report.compliance_rate:.1f}%")

    print(f"\nViolations by code:")
    for code, count in report.by_error_code.items():
        status = "OK" if count == 0 else f"{count} violations"
        print(f"  {code}: {status}")

    if report.violations:
        print(f"\n{'=' * 60}")
        print("VIOLATION DETAILS")
        print("=" * 60)

        for v in report.violations:
            print(f"\n[{v.error_code}] {v.skill_name}")
            print(f"  Path: {v.path}")
            print(f"  Issue: {v.issue}")
            print(f"  Fix: {v.suggestion}")
    else:
        print(f"\n{'=' * 60}")
        print("STATUS: PASSED - All skills comply with Golden Format")

    print("\n" + "=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate.py <plugin_path> [--json]")
        sys.exit(1)

    plugin_path = sys.argv[1]
    format = "json" if "--json" in sys.argv else "text"

    report = validate_plugin(plugin_path)
    print_report(report, format)

    sys.exit(0 if report.total_violations == 0 else 1)

if __name__ == "__main__":
    main()
