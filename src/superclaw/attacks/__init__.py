"""SuperClaw Attack Engine.

Attack implementations for testing AI agent security.
"""

from __future__ import annotations

from typing import Any

from superclaw.attacks.base import Attack, AttackResult
from superclaw.attacks.encoding import EncodingObfuscationAttack
from superclaw.attacks.jailbreaks import JailbreakAttack
from superclaw.attacks.multi_turn import MultiTurnAttack
from superclaw.attacks.prompt_injection import PromptInjectionAttack
from superclaw.attacks.tool_bypass import ToolBypassAttack

__all__ = [
    "Attack",
    "AttackResult",
    "PromptInjectionAttack",
    "EncodingObfuscationAttack",
    "JailbreakAttack",
    "ToolBypassAttack",
    "MultiTurnAttack",
    "ATTACK_REGISTRY",
    "run_attack",
    "run_evaluation",
    "run_audit",
]

ATTACK_REGISTRY = {
    "prompt-injection": PromptInjectionAttack,
    "encoding": EncodingObfuscationAttack,
    "jailbreak": JailbreakAttack,
    "tool-bypass": ToolBypassAttack,
    "multi-turn": MultiTurnAttack,
}


async def _run_attack_async(
    agent_type: str,
    target: str,
    behaviors: list[str] | None = None,
    techniques: list[str] | None = None,
    project_dir: str | None = None,
    adapter_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run attack asynchronously."""
    from superclaw.adapters import create_adapter
    from superclaw.behaviors import BEHAVIOR_REGISTRY, create_behavior
    from superclaw.config.settings import get_settings

    settings = get_settings()
    _enforce_guardrails(
        target=target,
        require_authorization=settings.safety_require_authorization,
        local_only=settings.safety_local_only,
        adapter_config=adapter_config,
    )

    config = {"target": target}
    if project_dir:
        config["project_dir"] = project_dir
    if adapter_config:
        config.update(adapter_config)

    adapter = create_adapter(agent_type, config)

    # Connect to agent
    connected = await adapter.connect()
    if not connected:
        return {"error": "Failed to connect to agent", "behaviors": {}}

    try:
        results = {
            "agent_type": agent_type,
            "target": target,
            "behaviors": {},
            "attacks": [],
            "overall_score": 0.0,
            "config": {
                "behaviors": behaviors,
                "techniques": techniques,
            },
        }

        # Determine which behaviors to test
        behavior_names = behaviors or list(BEHAVIOR_REGISTRY.keys())

        # Determine which techniques to use
        technique_names = techniques or list(ATTACK_REGISTRY.keys())

        # Run attacks
        for technique_name in technique_names:
            if technique_name not in ATTACK_REGISTRY:
                continue

            attack_class = ATTACK_REGISTRY[technique_name]
            attack = attack_class()

            # Generate attack payloads
            payloads = attack.generate_payloads()

            for payload in payloads[:5]:  # Limit payloads per technique
                # Send attack payload
                output = await adapter.send_prompt(payload)

                # Evaluate against behaviors
                for behavior_name in behavior_names:
                    if behavior_name not in BEHAVIOR_REGISTRY:
                        continue

                    behavior = create_behavior(behavior_name)
                    result = behavior.evaluate(output, context={})

                    # Aggregate results
                    if behavior_name not in results["behaviors"]:
                        results["behaviors"][behavior_name] = {
                            "passed": True,
                            "score": 1.0,
                            "evidence": [],
                            "attempts": 0,
                            "severity": result.severity.value,
                        }

                    behavior_results = results["behaviors"][behavior_name]
                    behavior_results["attempts"] += 1

                    if not result.passed:
                        behavior_results["passed"] = False
                        behavior_results["evidence"].extend(result.evidence)

                    # Running average score
                    n = behavior_results["attempts"]
                    behavior_results["score"] = (
                        behavior_results["score"] * (n - 1) + result.score
                    ) / n

                results["attacks"].append(
                    {
                        "technique": technique_name,
                        "payload_preview": payload[:100],
                        "response_length": len(output.response_text),
                        "evidence_ledger": output.to_ledger(),
                    }
                )

        # Calculate overall score
        if results["behaviors"]:
            scores = [b["score"] for b in results["behaviors"].values()]
            results["overall_score"] = sum(scores) / len(scores)

        results["findings"] = _build_findings(results["behaviors"])

        return results

    finally:
        await adapter.disconnect()


async def _run_evaluation_async(
    agent_type: str,
    target: str,
    scenarios: list[dict] | None = None,
    behaviors: list[str] | None = None,
    techniques: list[str] | None = None,
    project_dir: str | None = None,
    adapter_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run evaluation asynchronously, optionally using pre-generated scenarios."""
    from superclaw.adapters import create_adapter
    from superclaw.behaviors import BEHAVIOR_REGISTRY, create_behavior
    from superclaw.config.settings import get_settings

    settings = get_settings()
    _enforce_guardrails(
        target=target,
        require_authorization=settings.safety_require_authorization,
        local_only=settings.safety_local_only,
        adapter_config=adapter_config,
    )

    config = {"target": target}
    if project_dir:
        config["project_dir"] = project_dir
    if adapter_config:
        config.update(adapter_config)

    adapter = create_adapter(agent_type, config)

    connected = await adapter.connect()
    if not connected:
        return {"error": "Failed to connect to agent", "behaviors": {}, "scenarios": []}

    try:
        results = {
            "agent_type": agent_type,
            "target": target,
            "behaviors": {},
            "scenarios": [],
            "overall_score": 0.0,
            "config": {
                "behaviors": behaviors,
                "techniques": techniques,
            },
        }

        behavior_names = behaviors or list(BEHAVIOR_REGISTRY.keys())

        if not scenarios:
            return results

        for scenario in scenarios:
            prompt = scenario.get("prompt", "")
            output = await adapter.send_prompt(prompt, context={"scenario": scenario})

            scenario_behavior_results: dict[str, Any] = {}
            scenario_scores: list[float] = []
            scenario_passed = True

            scenario_behavior = scenario.get("behavior")
            if behaviors is None and scenario_behavior in BEHAVIOR_REGISTRY:
                active_behavior_names = [scenario_behavior]
            else:
                active_behavior_names = behavior_names

            for behavior_name in active_behavior_names:
                if behavior_name not in BEHAVIOR_REGISTRY:
                    continue

                behavior = create_behavior(behavior_name)
                result = behavior.evaluate(output, context={"scenario": scenario})

                scenario_behavior_results[behavior_name] = result.to_dict()
                scenario_scores.append(result.score)

                if not result.passed:
                    scenario_passed = False

                if behavior_name not in results["behaviors"]:
                    results["behaviors"][behavior_name] = {
                        "passed": True,
                        "score": 1.0,
                        "evidence": [],
                        "attempts": 0,
                        "severity": result.severity.value,
                    }

                behavior_results = results["behaviors"][behavior_name]
                behavior_results["attempts"] += 1

                if not result.passed:
                    behavior_results["passed"] = False
                    behavior_results["evidence"].extend(result.evidence)

                n = behavior_results["attempts"]
                behavior_results["score"] = (behavior_results["score"] * (n - 1) + result.score) / n

            scenario_score = sum(scenario_scores) / len(scenario_scores) if scenario_scores else 0.0

            results["scenarios"].append(
                {
                    "id": scenario.get("id"),
                    "behavior": scenario.get("behavior"),
                    "prompt": prompt,
                    "response_preview": output.response_text[:200],
                    "passed": scenario_passed,
                    "score": scenario_score,
                    "behaviors_evaluated": active_behavior_names,
                    "behavior_results": scenario_behavior_results,
                    "evidence_ledger": output.to_ledger(),
                }
            )

        if results["behaviors"]:
            scores = [b["score"] for b in results["behaviors"].values()]
            results["overall_score"] = sum(scores) / len(scores)

        results["findings"] = _build_findings(results["behaviors"])
        results["scenarios_tested"] = len(results["scenarios"])

        return results

    finally:
        await adapter.disconnect()


def run_attack(
    agent_type: str,
    target: str,
    behaviors: list[str] | None = None,
    techniques: list[str] | None = None,
    project_dir: str | None = None,
    adapter_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Run attack against an agent.

    Args:
        agent_type: Type of agent (openclaw, acp, etc.)
        target: Target URL or command
        behaviors: Behaviors to test (None = all)
        techniques: Attack techniques to use (None = all)
        project_dir: Project directory for ACP agents

    Returns:
        Attack results dictionary
    """
    import asyncio

    return asyncio.run(
        _run_attack_async(
            agent_type=agent_type,
            target=target,
            behaviors=behaviors,
            techniques=techniques,
            project_dir=project_dir,
            adapter_config=adapter_config,
        )
    )


def run_evaluation(
    agent_type: str,
    target: str,
    scenarios: list[dict] | None = None,
    behaviors: list[str] | None = None,
    techniques: list[str] | None = None,
    adapter_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Run evaluation against an agent.

    Similar to run_attack but with optional pre-generated scenarios.
    """
    import asyncio

    if scenarios:
        return asyncio.run(
            _run_evaluation_async(
                agent_type=agent_type,
                target=target,
                scenarios=scenarios,
                behaviors=behaviors,
                techniques=techniques,
                adapter_config=adapter_config,
            )
        )

    return run_attack(
        agent_type=agent_type,
        target=target,
        behaviors=behaviors,
        techniques=techniques,
        adapter_config=adapter_config,
    )


def run_audit(
    agent_type: str,
    target: str,
    mode: str = "standard",
) -> dict[str, Any]:
    """
    Run security audit against an agent.

    Args:
        agent_type: Type of agent
        target: Target URL
        mode: Audit mode (quick, standard, comprehensive)

    Returns:
        Audit results with summary
    """
    # Determine behaviors based on mode
    if mode == "quick":
        behaviors = ["prompt-injection-resistance", "tool-policy-enforcement"]
        techniques = ["prompt-injection"]
    elif mode == "comprehensive":
        behaviors = None  # All
        techniques = None  # All
    else:  # standard
        behaviors = [
            "prompt-injection-resistance",
            "tool-policy-enforcement",
            "sandbox-isolation",
        ]
        techniques = ["prompt-injection", "encoding", "tool-bypass"]

    results = run_attack(
        agent_type=agent_type,
        target=target,
        behaviors=behaviors,
        techniques=techniques,
    )

    results["summary"] = _build_summary(results.get("behaviors", {}))

    return results


def _build_summary(behavior_results: dict[str, Any]) -> dict[str, Any]:
    """Build a severity-aware summary from behavior results."""
    passed = sum(1 for b in behavior_results.values() if b.get("passed", False))
    failed = len(behavior_results) - passed

    severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for behavior in behavior_results.values():
        if not behavior.get("passed", False):
            severity = str(behavior.get("severity", "medium")).lower()
            if severity in severity_counts:
                severity_counts[severity] += 1

    return {
        "total_behaviors": len(behavior_results),
        "passed": passed,
        "failed": failed,
        "critical": severity_counts["critical"],
        "high": severity_counts["high"],
        "medium": severity_counts["medium"],
        "low": severity_counts["low"],
    }


def _build_findings(behavior_results: dict[str, Any]) -> list[dict[str, Any]]:
    """Build findings list for report generators."""
    from superclaw.behaviors import BEHAVIOR_REGISTRY, create_behavior

    findings = []
    for name, data in behavior_results.items():
        evidence = data.get("evidence", [])
        if isinstance(evidence, list):
            evidence_text = "; ".join(str(item) for item in evidence)
        else:
            evidence_text = str(evidence)

        contract: dict[str, Any] = {}
        if name in BEHAVIOR_REGISTRY:
            try:
                contract = create_behavior(name).get_contract_dict()
            except Exception:
                contract = {}

        findings.append(
            {
                "behavior": name,
                "status": "passed" if data.get("passed") else "failed",
                "severity": data.get("severity", "medium"),
                "score": data.get("score", 0.0),
                "evidence": evidence_text,
                "intent": contract.get("intent"),
                "mitigation": contract.get("mitigation"),
                "success_criteria": contract.get("success_criteria", []),
                "severity_rubric": contract.get("severity_rubric", []),
            }
        )
    return findings


def _enforce_guardrails(
    target: str,
    require_authorization: bool,
    local_only: bool,
    adapter_config: dict[str, Any] | None,
) -> None:
    """Enforce local-only and authorization guardrails."""
    import os

    if local_only and not _is_local_target(target):
        raise ValueError("Local-only mode is enabled; remote targets are blocked.")

    if require_authorization and not _is_local_target(target):
        token = None
        if adapter_config:
            token = adapter_config.get("authorization_token") or adapter_config.get("token")
        token = token or os.environ.get("SUPERCLAW_AUTH_TOKEN")
        if not token:
            raise ValueError(
                "Authorization required for remote targets. Set SUPERCLAW_AUTH_TOKEN "
                "or pass adapter token."
            )


def _is_local_target(target: str) -> bool:
    """Check whether the target is local/private."""
    from ipaddress import ip_address, ip_network
    from urllib.parse import urlparse

    if not isinstance(target, str):
        return True
    if target.startswith(("ws://", "wss://", "http://", "https://")):
        parsed = urlparse(target)
        host = parsed.hostname
        if not host:
            return True
        if host in {"localhost", "127.0.0.1", "::1"}:
            return True
        try:
            ip = ip_address(host)
        except ValueError:
            return False
        private_networks = [
            ip_network("10.0.0.0/8"),
            ip_network("172.16.0.0/12"),
            ip_network("192.168.0.0/16"),
            ip_network("127.0.0.0/8"),
            ip_network("::1/128"),
        ]
        return any(ip in net for net in private_networks)
    # Non-URL targets (e.g., commands) are treated as local
    return True
