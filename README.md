# Goose MCP Escrow Server

A minimal, deterministic MCP server implementing an escrow-style planning architecture for Goose agents. This server enables safe, auditable, and reversible task execution through explicit separation of intent formation, verification, planning, and settlement.

---

## Overview

The Goose MCP Escrow Server provides a structured framework for autonomous agents to:
- **Parse and normalize** user intents into canonical representations
- **Verify** intents against configurable safety constraints
- **Generate deterministic plans** that are reproducible and auditable
- **Execute or rollback** plans with explicit confirmation semantics

This architecture draws inspiration from programmable settlement systems and Web3 intent-based protocols (WAP3), adapted for general-purpose agentic workflows. By separating intent declaration from execution, agents gain a safe container for reasoning about actions before commitment.

---

## Core Design Principles

### Intent Separation
User input is transformed into a structured intent schema, decoupling what the user wants from how it will be executed.

### Deterministic Planning
Given identical input, the planner produces identical output. This enables:
- **Reproducible debugging** across different environments
- **Cryptographic auditability** (future extension)
- **Predictable agent behavior** for complex workflows

### Verification Before Execution
Lightweight safety guardrails validate:
- Whitelisted actions only
- Non-negative resource amounts
- Explicit risk level declarations

### Reversible Execution
Every plan can be committed or rolled back, providing:
- Safe experimentation in agent workflows
- Explicit human-in-the-loop approval gates
- Rollback semantics for multi-step transactions

---

## MCP Interface

The server exposes two primary tools:

### `escrow_plan`
**Input**: Raw user intent
```json
{
  "action": "allocate",
  "target": "resource_1",
  "amount": 100,
  "risk_level": "low"
}
```

**Output**: Deterministic plan with unique identifier
```json
{
  "plan_id": "uuid-v4",
  "intent": { ... },
  "constraints": { "risk_level": "low", "max_retries": 1 },
  "steps": [ ... ],
  "explain": "Human-readable plan description"
}
```

### `escrow_execute`
**Input**: Plan confirmation
```json
{
  "plan_id": "uuid-v4",
  "confirm": true
}
```

**Output**: Execution result
```json
{
  "plan_id": "uuid-v4",
  "status": "committed"
}
```

---

## Architecture

```
goose-mcp-escrow-server/
├── server.py                    # MCP entrypoint with file/stdin modes
├── mcp.json                     # MCP server configuration
├── requirements.txt             # Zero external dependencies
├── escrow/
│   ├── __init__.py
│   ├── intent.py                # Intent normalization
│   ├── verify.py                # Safety verification
│   ├── planner.py               # Deterministic plan generation
│   └── executor.py              # Plan registration & execution
└── examples/
    ├── request_plan.json
    └── request_execute.json
```

### Data Flow

```
User Input -> Intent Parser -> Verifier -> Planner -> Executor
                                  |           |         |
                             Guardrails    Plan DB  Settlement
```

---

## Quick Start

### Installation
```bash
git clone https://github.com/yourusername/goose-mcp-escrow-server.git
cd goose-mcp-escrow-server
```

No dependencies required—uses Python standard library only.

### Test Workflow

**Step 1: Generate a Plan**
```bash
python server.py examples/request_plan.json
```

**Sample Output:**
```json
{
  "plan": {
    "plan_id": "5c93310c-2b57-4a3e-8364-b3b901edbd03",
    "intent": {
      "action": "allocate",
      "target": "resource_1",
      "amount": 100,
      "risk_level": "low"
    },
    "constraints": {
      "risk_level": "low",
      "max_retries": 1
    },
    "steps": [
      {"step": "check_constraints", "ok": true},
      {"step": "prepare_execution", "ok": true}
    ],
    "explain": "Planned allocate toward resource_1 with risk level low"
  }
}
```

**Step 2: Update Execution Request**

Edit `examples/request_execute.json` with the returned `plan_id`:
```json
{
  "tool": "escrow_execute",
  "input": {
    "plan_id": "5c93310c-2b57-4a3e-8364-b3b901edbd03",
    "confirm": true
  }
}
```

**Step 3: Execute the Plan**
```bash
python server.py examples/request_execute.json
```

**Output:**
```json
{
  "result": {
    "plan_id": "5c93310c-2b57-4a3e-8364-b3b901edbd03",
    "status": "committed"
  }
}
```

### Negative Test Cases

**Invalid Action:**
```bash
echo '{"tool":"escrow_plan","input":{"action":"fly_to_mars","target":"mars","risk_level":"low"}}' | python server.py
```
Returns: `{"error": "intent_validation_failed", "detail": "Unsupported action: fly_to_mars"}`

**Negative Amount:**
```bash
echo '{"tool":"escrow_plan","input":{"action":"allocate","target":"test","amount":-5,"risk_level":"low"}}' | python server.py
```
Returns: `{"error": "intent_validation_failed", "detail": "Amount must not be negative"}`

---

## Why Escrow-Style Planning?

This pattern addresses fundamental challenges in autonomous agent systems:

| Challenge | Solution |
|-----------|----------|
| **Unpredictable agent behavior** | Deterministic planning guarantees reproducibility |
| **Safety concerns** | Explicit verification layer with whitelist policies |
| **Difficult debugging** | Plans are JSON-serializable and human-readable |
| **Irreversible actions** | Rollback semantics built into execution model |
| **Auditability gaps** | Every plan has UUID and structured logging |

### Comparison to Traditional Approaches

**Direct Execution (LangChain/AutoGPT style):**
```
Intent -> Action (immediate, irreversible, opaque)
```

**Escrow Planning:**
```
Intent -> Verify -> Plan -> Review -> Commit/Rollback
           |        |       |        |
      Guardrails  UUID  Explain  Settlement
```

---

## Integration Scenarios

### 1. Goose Agent Workflows
```python
# Agent generates plan
plan = agent.use_tool("escrow_plan", {
    "action": "schedule",
    "target": "deployment_pipeline",
    "risk_level": "medium"
})

# Human reviews plan explanation
if human_approves(plan["explain"]):
    agent.use_tool("escrow_execute", {
        "plan_id": plan["plan_id"],
        "confirm": True
    })
```

### 2. Multi-Agent Coordination
```
Agent A -> Creates Plan -> Stores plan_id
Agent B -> Reads plan_id -> Reviews constraints
Agent B -> Executes plan -> Returns result to A
```

### 3. Approval Workflows
```
Junior Agent -> Generates plan
Senior Agent -> Reviews plan.explain
Senior Agent -> Confirms or rejects via escrow_execute
```

---

## Technical Specifications

### Supported Actions
- `allocate` - Resource allocation operations
- `schedule` - Task scheduling operations
- `approve` - Approval workflow steps
- `release` - Resource release operations

### Risk Levels
- `low` - 1 retry, minimal constraints
- `medium` - 2 retries, standard constraints
- `high` - 2 retries, strict validation (extensible)

### Persistence
Plans and executions are persisted to local JSON files (`plans.json`, `executions.json`) for demonstration purposes. Production deployments should integrate with durable storage backends.

---

## Extensibility

The modular architecture supports:

**Custom Verifiers:**
```python
# escrow/verify.py
def verify_intent(intent):
    # Add domain-specific validation
    if intent["action"] == "transfer":
        check_balance(intent["amount"])
```

**Policy-Based Planning:**
```python
# escrow/planner.py
def build_plan(intent):
    policy = load_policy(intent["risk_level"])
    return apply_policy_constraints(intent, policy)
```

**Cryptographic Audit Logs:**
```python
# Future extension
plan["signature"] = sign(plan, private_key)
plan["merkle_root"] = build_merkle_tree(plan["steps"])
```

---

## Roadmap

### Phase 1: Core Functionality ✅
- [x] Intent parsing and normalization
- [x] Deterministic plan generation
- [x] Commit/rollback semantics
- [x] File and stdin input modes
- [x] Persistent plan storage

### Phase 2: Enhanced Verification
- [ ] Pluggable validation policies
- [ ] Custom constraint languages (e.g., Rego)
- [ ] Risk scoring models
- [ ] Multi-signature approval flows

### Phase 3: Production Hardening
- [ ] Database backend (PostgreSQL/SQLite)
- [ ] Cryptographic audit logging
- [ ] Plan expiration and TTL
- [ ] Distributed plan coordination

### Phase 4: Advanced Features
- [ ] Multi-step plan orchestration
- [ ] Conditional execution (if-then-else)
- [ ] Plan composition and nesting
- [ ] Integration with settlement layers (blockchain, payment rails)

---

## Design Philosophy

This project embodies principles from:

### Intent-Centric Architecture (WAP3)
Separating *what* users want from *how* it's executed enables:
- Cross-domain plan portability
- Solver competition (multiple planners can bid on the same intent)
- Upgradeable execution without changing user interfaces

### Verifiable Computation
Deterministic planning ensures:
- Plans can be recomputed and verified by third parties
- Debugging is reproducible across environments
- Compliance audits have cryptographic proof

### Programmable Settlement
Explicit commit/rollback semantics mirror:
- Two-phase commit protocols in distributed systems
- Escrow mechanisms in financial systems
- State channels in blockchain systems

---

## Contributing

Contributions are welcome! Areas of interest:

- **Verification policies** for specific domains (finance, DevOps, data pipelines)
- **Planner strategies** optimizing for cost, time, or reliability
- **Integration adapters** for popular agent frameworks
- **Audit tooling** for plan analysis and visualization

Please open issues for bugs or feature requests, and submit PRs with tests.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

This project is built for the [Goose](https://github.com/square/goose) open-source ecosystem, which provides developer-friendly AI agents with MCP integration.

The escrow planning pattern is inspired by work on verifiable agent workflows, programmable settlement systems, and intent-based protocols in decentralized systems.

---

## Contact

For questions, collaboration, or grant inquiries:
- GitHub Issues: [github.com/nelsonjingusc/goose-mcp-escrow-server/issues]
- Email: nelson.jingusc@gmail.com
- Telegram: @nelsonjingusc

---

**Built for safer, more transparent autonomous agents.**