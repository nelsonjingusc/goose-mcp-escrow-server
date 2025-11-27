from typing import Any, Dict


def parse_intent(data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize raw input into a structured intent."""
    return {
        "action": data["action"],
        "target": data["target"],
        "amount": data.get("amount"),
        "risk_level": data.get("risk_level", "medium"),
    }