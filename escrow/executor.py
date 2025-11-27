import json
import os
from typing import Dict, Any

# Persistent storage file
PLANS_FILE = "plans.json"
EXECUTIONS_FILE = "executions.json"


def _load_plans() -> Dict[str, Dict[str, Any]]:
    """Load plans from JSON file."""
    if not os.path.exists(PLANS_FILE):
        return {}
    try:
        with open(PLANS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_plans(plans: Dict[str, Dict[str, Any]]) -> None:
    """Save plans to JSON file."""
    with open(PLANS_FILE, 'w') as f:
        json.dump(plans, f, indent=2)


def _load_executions() -> Dict[str, Dict[str, Any]]:
    """Load executions from JSON file."""
    if not os.path.exists(EXECUTIONS_FILE):
        return {}
    try:
        with open(EXECUTIONS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_executions(executions: Dict[str, Dict[str, Any]]) -> None:
    """Save executions to JSON file."""
    with open(EXECUTIONS_FILE, 'w') as f:
        json.dump(executions, f, indent=2)


def register_plan(plan: Dict[str, Any]) -> None:
    """Store the plan in persistent storage for later execution."""
    plan_id = plan["plan_id"]
    plans = _load_plans()
    plans[plan_id] = plan
    _save_plans(plans)


def execute_plan(plan_id: str, confirm: bool) -> Dict[str, Any]:
    """Simulate commit or rollback of a planned action."""
    plans = _load_plans()
    if plan_id not in plans:
        raise ValueError(f"Unknown plan id: {plan_id}")

    status = "committed" if confirm else "rolled_back"
    result = {"plan_id": plan_id, "status": status}

    executions = _load_executions()
    executions[plan_id] = result
    _save_executions(executions)

    return result