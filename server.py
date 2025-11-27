import json
import sys
from typing import Any, Dict

from escrow.intent import parse_intent
from escrow.verify import verify_intent, IntentValidationError
from escrow.planner import build_plan
from escrow.executor import register_plan, execute_plan


def handle_call(tool: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Dispatch MCP tool calls to internal handlers."""

    if tool == "escrow_plan":
        intent = parse_intent(input_data)
        verify_intent(intent)
        plan = build_plan(intent)
        register_plan(plan)
        return {"plan": plan}

    if tool == "escrow_execute":
        result = execute_plan(
            plan_id=input_data["plan_id"],
            confirm=input_data["confirm"],
        )
        return {"result": result}

    return {"error": f"Unknown tool: {tool}"}


def main() -> None:
    """Minimal loop for testing MCP style requests through file or stdin."""
    # Support both file mode and stdin mode
    if len(sys.argv) > 1:
        # File mode: python server.py <path_to_json_file>
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                raw = f.read()
        except FileNotFoundError:
            print(json.dumps({"error": f"File not found: {file_path}"}))
            return
        except Exception as exc:
            print(json.dumps({"error": "file_read_error", "detail": str(exc)}))
            return
    else:
        # Stdin mode: python server.py < request.json
        raw = sys.stdin.read()

    if not raw:
        print(json.dumps({"error": "No input"}))
        return

    try:
        request = json.loads(raw)
    except json.JSONDecodeError:
        print(json.dumps({"error": "Invalid JSON"}))
        return

    tool = request.get("tool")
    input_data = request.get("input", {})

    try:
        response = handle_call(tool, input_data)
    except IntentValidationError as exc:
        response = {"error": "intent_validation_failed", "detail": str(exc)}
    except Exception as exc:
        response = {"error": "server_error", "detail": str(exc)}

    print(json.dumps(response))


if __name__ == "__main__":
    main()