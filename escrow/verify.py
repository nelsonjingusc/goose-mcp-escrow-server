from typing import Dict, Any


class IntentValidationError(ValueError):
    """Raised when an intent fails safety checks."""


def verify_intent(intent: Dict[str, Any]) -> None:
    """Apply basic safety checks on the intent."""

    allowed_actions = {"allocate", "schedule", "approve", "release"}
    allowed_risks = {"low", "medium", "high"}

    action = intent["action"]
    risk = intent["risk_level"]
    amount = intent.get("amount")

    if action not in allowed_actions:
        raise IntentValidationError(f"Unsupported action: {action}")

    if risk not in allowed_risks:
        raise IntentValidationError(f"Invalid risk level: {risk}")

    if amount is not None and amount < 0:
        raise IntentValidationError("Amount must not be negative")