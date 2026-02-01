"""Drift analysis between two SuperClaw runs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DriftConfig:
    """Configuration for drift detection."""

    score_drop_threshold: float = 0.1


def compare_runs(
    baseline: dict[str, Any],
    current: dict[str, Any],
    config: DriftConfig | None = None,
) -> dict[str, Any]:
    """Compare two SuperClaw results dictionaries."""
    config = config or DriftConfig()

    baseline_behaviors = baseline.get("behaviors", {}) or {}
    current_behaviors = current.get("behaviors", {}) or {}

    behavior_names = sorted(set(baseline_behaviors) | set(current_behaviors))

    behavior_diffs = []
    regressions = 0
    improvements = 0

    for name in behavior_names:
        base = baseline_behaviors.get(name, {})
        cur = current_behaviors.get(name, {})

        base_score = float(base.get("score", 0.0))
        cur_score = float(cur.get("score", 0.0))
        delta = cur_score - base_score

        base_passed = bool(base.get("passed", False))
        cur_passed = bool(cur.get("passed", False))

        status_change = "unchanged"
        if base_passed and not cur_passed:
            status_change = "regression"
            regressions += 1
        elif not base_passed and cur_passed:
            status_change = "improvement"
            improvements += 1
        elif delta <= -config.score_drop_threshold:
            status_change = "score_drop"
            regressions += 1
        elif delta >= config.score_drop_threshold:
            status_change = "score_gain"
            improvements += 1

        behavior_diffs.append(
            {
                "behavior": name,
                "baseline_score": base_score,
                "current_score": cur_score,
                "delta": round(delta, 3),
                "baseline_passed": base_passed,
                "current_passed": cur_passed,
                "status_change": status_change,
                "severity": cur.get("severity", base.get("severity", "medium")),
            }
        )

    scenario_diffs = _compare_scenarios(baseline.get("scenarios", []), current.get("scenarios", []))

    summary = {
        "behaviors_total": len(behavior_names),
        "regressions": regressions,
        "improvements": improvements,
        "score_drop_threshold": config.score_drop_threshold,
        "scenarios_total": len(scenario_diffs),
        "scenario_regressions": sum(1 for s in scenario_diffs if s["status_change"] == "regression"),
        "scenario_improvements": sum(1 for s in scenario_diffs if s["status_change"] == "improvement"),
    }

    return {
        "summary": summary,
        "behavior_diffs": behavior_diffs,
        "scenario_diffs": scenario_diffs,
        "baseline_run": _run_id(baseline),
        "current_run": _run_id(current),
    }


def _compare_scenarios(
    baseline_scenarios: list[dict[str, Any]],
    current_scenarios: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    baseline_map = {s.get("id"): s for s in baseline_scenarios if s.get("id")}
    current_map = {s.get("id"): s for s in current_scenarios if s.get("id")}

    scenario_ids = sorted(set(baseline_map) | set(current_map))
    diffs = []

    for scenario_id in scenario_ids:
        base = baseline_map.get(scenario_id, {})
        cur = current_map.get(scenario_id, {})

        base_passed = bool(base.get("passed", False))
        cur_passed = bool(cur.get("passed", False))

        status_change = "unchanged"
        if base_passed and not cur_passed:
            status_change = "regression"
        elif not base_passed and cur_passed:
            status_change = "improvement"

        diffs.append(
            {
                "scenario_id": scenario_id,
                "behavior": cur.get("behavior", base.get("behavior")),
                "baseline_passed": base_passed,
                "current_passed": cur_passed,
                "baseline_score": float(base.get("score", 0.0)),
                "current_score": float(cur.get("score", 0.0)),
                "status_change": status_change,
            }
        )

    return diffs


def _run_id(results: dict[str, Any]) -> str | None:
    metadata = results.get("metadata", {}) or {}
    return metadata.get("run_id")
