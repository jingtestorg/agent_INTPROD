# Specification: greeting-onboarding-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read the project input (`product-requirements-document.md` and `intent.md`)
- [x] Bootstrap agent code in `assets/greeting-onboarding-agent/` using instructions from the sap-agent-bootstrap section
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

- [x] Evaluate whether a runtime skill is appropriate for the onboarding flow — YES, a runtime skill is appropriate
- [x] Create `assets/greeting-onboarding-agent/app/skills/onboarding-flow/SKILL.md` with 5 sequential onboarding steps

---

## Project-Specific Tasks

### System Prompt — Greeting & Persona

- [x] Updated `get_system_prompt()` in `app/agent.py` with agent identity, tone, scope guardrail, off-topic handling, and runtime skill loading instruction

### R1 — Personalised Greeting

- [x] System prompt instructs agent to introduce itself at start of every conversation
- [x] Agent's opening message asks for the employee's name
- [x] Agent uses employee's name in subsequent messages

### R2 — Role Collection

- [x] Agent asks for role after collecting name
- [x] Role stored in conversation context

### R3 — Step-by-Step Onboarding Guidance

- [x] Agent loads `onboarding-flow` skill and begins walkthrough once name and role collected
- [x] Agent presents one step at a time and waits for acknowledgement
- [x] Agent handles mid-flow questions and resumes
- [x] Agent does not skip or present all steps at once

### R4 — Completion Confirmation

- [x] Agent delivers explicit completion message after all steps acknowledged

### R5 — Graceful Handling of Off-Topic Input

- [x] Agent acknowledges off-topic input politely and redirects to onboarding flow
- [x] Tested with off-topic example ("What is the weather today?")

---

## Business Instrumentation

- [x] M1, M2, M3 milestone log statements implemented in `_run_agent()` helper
- [x] OpenTelemetry span `onboarding-agent-turn` added in `_run_agent()`
- [x] Business logic extracted from `stream()` into `_run_agent()` to avoid GeneratorExit errors
- [x] `bootstrap(app)` called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

- [x] `asset.yaml` has no `requires` entries — no MCP servers needed
- [x] `app/agent.py` contains no direct HTTP clients or SAP API calls

---

## Testing

- [x] `conftest.py` sets `IBD_TESTING=true`
- [x] Unit tests written in `assets/greeting-onboarding-agent/tests/test_greeting_agent.py`
- [x] Integration test for full onboarding flow written
- [x] All 108 tests pass, coverage = 70%
- [x] `test_report.json` exists in `assets/greeting-onboarding-agent/`
