import uuid
from typing import Dict, Any


def build_plan(intent: Dict[str, Any]) -> Dict[str, Any]:
    """Build a deterministic plan from a verified intent."""

    plan_id = str(uuid.uuid4())

    risk = intent["risk_level"]
    constraints = {
        "risk_level": risk,
        "max_retries": 1 if risk == "low" else 2,
    }

    steps = [
        {"step": "check_constraints", "ok": True},
        {"step": "prepare_execution", "ok": True},
    ]

    explain = (
        f"Planned {intent['action']} toward {intent['target']} "
        f"with risk level {risk}"
    )

    return {
        "plan_id": plan_id,
        "intent": intent,
        "constraints": constraints,
        "steps": steps,
        "explain": explain,
    }