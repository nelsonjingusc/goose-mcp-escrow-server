# Goose MCP Escrow Server

A minimal MCP server that provides escrow style intent verification, deterministic planning, and reversible execution for Goose agents. The server separates intent parsing, verification, planning, and commit or rollback actions in a clear and auditable workflow.

## Features

- Structured intent schema
- Deterministic plan generation
- Lightweight verification rules
- Commit and rollback execution
- Zero external dependencies
- Native MCP tool definitions

## Repository Structure

```
goose-mcp-escrow-server/
  server.py
  mcp.json
  requirements.txt
  README.md
  escrow/
    __init__.py
    intent.py
    verify.py
    planner.py
    executor.py
  examples/
    request_plan.json
    request_execute.json
```

## MCP Tools

### `escrow_plan`

Parses user intent, applies guardrails, and returns a deterministic plan.

**Input**
```json
{
  "action": "allocate",
  "target": "resource_1",
  "amount": 100,
  "risk_level": "low"
}
```

**Output**
```json
{
  "plan_id": "uuid",
  "intent": { ... },
  "constraints": { "risk_level": "low", "max_retries": 1 },
  "steps": [ ... ],
  "explain": "Planned allocate toward resource_1 with risk level low"
}
```

### `escrow_execute`

Confirms or rolls back a previously generated plan.

**Input**
```json
{
  "plan_id": "uuid",
  "confirm": true
}
```

**Output**
```json
{
  "plan_id": "uuid",
  "status": "committed"
}
```

## Quick Test

### 1. Generate a plan
```
python server.py examples/request_plan.json
```

### 2. Edit `examples/request_execute.json`

Replace `plan_id` with the returned value.

### 3. Execute the plan
```
python server.py examples/request_execute.json
```

## Design

- User intent is normalized before any logic is applied.
- Verification applies simple safety rules.
- Planning is deterministic so results can be reproduced.
- Execution supports commit or rollback.

## License

MIT License.