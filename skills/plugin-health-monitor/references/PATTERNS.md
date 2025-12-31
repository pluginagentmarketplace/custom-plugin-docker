# Plugin Health Monitor Patterns

Design patterns and best practices for health monitoring and scoring.

## Scoring Patterns

### Pattern 1: Weighted Multi-Factor

Apply different weights to different factors:

```python
def calculate_weighted_score(factors: Dict[str, float]) -> float:
    """
    Calculate weighted health score.

    Weights:
    - structure: 25%
    - syntax: 20%
    - mcp: 15%
    - loading: 25%
    - stability: 15%
    """
    weights = {
        'structure': 0.25,
        'syntax': 0.20,
        'mcp': 0.15,
        'loading': 0.25,
        'stability': 0.15
    }

    total = 0
    for factor, score in factors.items():
        if factor in weights:
            total += score * weights[factor]

    return round(total, 1)
```

### Pattern 2: Threshold-Based Status

Map scores to status levels:

```python
def get_health_status(score: float) -> Tuple[str, str]:
    """
    Get status and color based on score.

    Returns: (status, color)
    """
    if score >= 85:
        return "HEALTHY", "green"
    elif score >= 70:
        return "WARNING", "yellow"
    elif score >= 50:
        return "CRITICAL", "orange"
    else:
        return "FAILING", "red"
```

### Pattern 3: Factor Breakdown

Provide detailed breakdown of each factor:

```python
@dataclass
class FactorScore:
    name: str
    score: float
    weight: float
    issues: List[str]
    contribution: float

    @property
    def weighted_score(self) -> float:
        return self.score * self.weight

def analyze_factors(plugin_path: Path) -> List[FactorScore]:
    """Analyze each health factor separately"""
    factors = []

    # Structure factor
    struct_score, struct_issues = check_structure(plugin_path)
    factors.append(FactorScore(
        name="structure",
        score=struct_score,
        weight=0.25,
        issues=struct_issues,
        contribution=struct_score * 0.25
    ))

    # Continue for other factors...
    return factors
```

## Monitoring Patterns

### Pattern 1: Continuous Monitoring

Monitor health over time:

```python
class HealthMonitor:
    def __init__(self, plugin_path: Path, interval: int = 300):
        self.plugin_path = plugin_path
        self.interval = interval
        self.history = []

    def check(self) -> HealthScore:
        """Perform health check and record"""
        score = calculate_health(self.plugin_path)
        self.history.append({
            "timestamp": datetime.now(),
            "score": score.total,
            "status": score.status
        })
        return score

    def get_trend(self, hours: int = 24) -> str:
        """Analyze trend over time"""
        recent = [h for h in self.history
                  if h["timestamp"] > datetime.now() - timedelta(hours=hours)]

        if len(recent) < 2:
            return "insufficient_data"

        first = recent[0]["score"]
        last = recent[-1]["score"]

        if last > first + 5:
            return "improving"
        elif last < first - 5:
            return "degrading"
        else:
            return "stable"
```

### Pattern 2: Alert Thresholds

Trigger alerts based on thresholds:

```python
class AlertManager:
    def __init__(self):
        self.thresholds = {
            "critical": 50,
            "warning": 70,
            "degradation": 10  # Score drop
        }
        self.last_score = None

    def check_alerts(self, current_score: float) -> List[Alert]:
        alerts = []

        # Absolute thresholds
        if current_score < self.thresholds["critical"]:
            alerts.append(Alert("CRITICAL", f"Score below {self.thresholds['critical']}"))
        elif current_score < self.thresholds["warning"]:
            alerts.append(Alert("WARNING", f"Score below {self.thresholds['warning']}"))

        # Relative change
        if self.last_score:
            drop = self.last_score - current_score
            if drop >= self.thresholds["degradation"]:
                alerts.append(Alert("DEGRADATION", f"Score dropped by {drop}"))

        self.last_score = current_score
        return alerts
```

### Pattern 3: Scheduled Checks

Run checks on schedule:

```python
import schedule

def setup_monitoring(plugin_path: Path):
    """Setup scheduled health monitoring"""

    def quick_check():
        score = quick_health_check(plugin_path)
        if score.status in ["CRITICAL", "FAILING"]:
            send_alert(score)

    def full_check():
        score = full_health_check(plugin_path)
        save_to_history(score)
        generate_report(score)

    # Quick check every 15 minutes
    schedule.every(15).minutes.do(quick_check)

    # Full check every hour
    schedule.every().hour.do(full_check)

    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)
```

## Reporting Patterns

### Dashboard Format

```python
def generate_dashboard(score: HealthScore) -> str:
    """Generate health dashboard output"""
    lines = [
        "=" * 60,
        f"PLUGIN HEALTH REPORT: {score.plugin_name}",
        "=" * 60,
        "",
        f"Overall Score: {score.total}/100 [{score.status}]",
        "",
        "Component Scores:"
    ]

    for factor in score.factors:
        status = "[OK]" if factor.score >= 85 else "[WARN]" if factor.score >= 70 else "[FAIL]"
        lines.append(f"  {factor.name.capitalize():12} {factor.score:5.1f}/100 {status}")

    if score.issues:
        lines.extend(["", "Issues Found:"])
        for issue in score.issues[:5]:
            lines.append(f"  - {issue}")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
```

### JSON Export

```python
def export_to_json(score: HealthScore) -> str:
    """Export health score as JSON"""
    return json.dumps({
        "plugin": score.plugin_name,
        "timestamp": datetime.now().isoformat(),
        "overall_score": score.total,
        "status": score.status,
        "factors": {
            f.name: {
                "score": f.score,
                "weight": f.weight,
                "contribution": f.contribution
            }
            for f in score.factors
        },
        "issues": [i.to_dict() for i in score.issues]
    }, indent=2)
```

## Anti-Patterns

### Anti-Pattern 1: Binary Health

```python
# BAD - Only healthy or not
def bad_health(plugin_path):
    return check_all_ok(plugin_path)  # True/False only

# GOOD - Graduated scoring
def good_health(plugin_path):
    return calculate_score(plugin_path)  # 0-100 with details
```

### Anti-Pattern 2: Ignoring Trends

```python
# BAD - Only current state
def bad_monitor(plugin_path):
    return current_score(plugin_path)

# GOOD - Include history and trends
def good_monitor(plugin_path):
    current = current_score(plugin_path)
    history = get_history(plugin_path)
    trend = calculate_trend(history)

    return {
        "current": current,
        "trend": trend,
        "history": history[-10:]  # Last 10 checks
    }
```

## See Also

- [HEALTH-GUIDE.md](HEALTH-GUIDE.md)
- [SKILL.md](../SKILL.md)
- [Error Codes Reference](../../../references/ERROR-CODES.md)

---

Generated by plugin-health-agent
