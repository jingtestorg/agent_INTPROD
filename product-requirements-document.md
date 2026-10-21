# Product Requirements Document (PRD)

**Title:** Simple Greeting & Onboarding Agent
**Date:** 2026-10-21
**Owner:** HR / Onboarding Team
**Solution Category:** AI Agent

---

## Product Purpose & Value Proposition

**Elevator Pitch:**
New employees today spend 3–5 days navigating fragmented onboarding information with no guided support. This AI agent greets them personally, walks them through every onboarding step in a natural conversation, and confirms they are ready to start — cutting that time in half.

**Business Need:**
The current onboarding process requires new hires to self-navigate across multiple sources (documents, emails, portals) without a unified, interactive guide. This leads to delays, inconsistency, and a poor first impression. An intelligent conversational agent fills this gap without requiring any system integration.

**Expected Value:**
- Onboarding completion time reduced from 3–5 days to 1.5–2.5 days (50% improvement)
- Consistent onboarding experience for every new employee
- Reduced coordination burden on HR coordinators

**Product Objectives (Prioritized):**
1. Deliver a conversational onboarding experience that guides employees step-by-step without manual HR involvement
2. Confirm successful completion of all onboarding steps in a single interaction
3. Provide a foundation that HR can extend with additional onboarding content over time

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Onboarding completion time | 3–5 days | 50% faster (1.5–2.5 days) | — | Employee Onboarding | user |

---

## User Profiles & Personas

### Primary Persona: Alex — New Employee

Alex is a 27-year-old professional joining the company in a non-technical role. It is their first day and they have received a welcome email with a link to the onboarding agent. Alex is comfortable with messaging apps and expects a helpful, clear experience. Their biggest frustration is not knowing what to do next or where to find information. Alex needs the agent to feel like a knowledgeable, friendly guide — not a rigid checklist system.

**Goals:**
- Understand what steps to complete on day one and day two
- Get answers to simple questions without having to email HR
- Feel confident and prepared to start work

**Key Tasks:**
- Introduce themselves to the agent
- Follow the onboarding steps as guided
- Confirm completion and know what comes next

### Secondary Persona: Jordan — HR / Onboarding Coordinator

Jordan is a 35-year-old HR specialist responsible for onboarding 10–20 new hires per month. Today, Jordan manually answers the same onboarding questions repeatedly and has to follow up with employees who missed steps. Jordan wants onboarding to be self-service and consistent, freeing up time for more strategic HR work. Jordan is not a developer but expects to be able to update onboarding content without technical help.

**Goals:**
- Ensure every new hire completes onboarding without manual follow-up
- Maintain accurate, up-to-date onboarding content in the agent

---

## Goals and Non-Goals

### Goals (In Scope)

- Greet new employees personally and introduce the agent's purpose
- Collect the employee's name and role at the start of the conversation
- Guide the employee through all required onboarding steps conversationally
- Confirm completion and signal that the employee is ready to start
- Handle off-topic or unclear inputs gracefully

### Non-Goals (Out of Scope)

- Integration with HR systems (e.g., SAP SuccessFactors, payroll, identity management)
- Document signing or form submission workflows
- Manager or approver notification flows
- Multilingual support (initial release in English only)

---

## Requirements

### Must-Have Requirements

**R1: Personalised Greeting**
- **Problem to Solve:** Employees feel anonymous and unwelcome when onboarding starts with a generic form or portal.
- **User Story:** As a new employee, I need the agent to greet me by name so that I feel welcomed and know who I am talking to.
- **Acceptance Criteria:**
  - Given the conversation starts, when the agent responds, then it introduces itself and asks for the employee's name.
  - Given the employee provides their name, when the agent acknowledges it, then all subsequent messages use that name.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 1

**R2: Role Collection**
- **Problem to Solve:** Onboarding steps can vary by role; the agent needs to know the employee's role to provide relevant guidance.
- **User Story:** As a new employee, I need the agent to ask about my role so that the guidance I receive is relevant to my position.
- **Acceptance Criteria:**
  - Given the agent has collected the employee's name, when it continues the conversation, then it asks for the employee's role or department.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 2

**R3: Step-by-Step Onboarding Guidance**
- **Problem to Solve:** Employees do not know the sequence of onboarding steps and often miss important ones.
- **User Story:** As a new employee, I need the agent to walk me through each onboarding step one at a time so that I complete them all in the correct order.
- **Acceptance Criteria:**
  - Given the agent knows the employee's name and role, when the walkthrough begins, then the agent presents onboarding steps sequentially.
  - Given the employee acknowledges completing a step, when the agent responds, then it moves to the next step.
  - Given an employee asks a question mid-flow, when the agent responds, then it answers and resumes the onboarding flow.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 3

**R4: Completion Confirmation**
- **Problem to Solve:** Employees are unsure whether they have finished onboarding or if further action is required.
- **User Story:** As a new employee, I need the agent to confirm when I have completed all steps so that I know I am ready to start.
- **Acceptance Criteria:**
  - Given all onboarding steps have been covered, when the agent reaches the end of the flow, then it explicitly confirms completion and provides a closing message.
- **Maps to Objective:** Objective 2
- **Priority Rank:** 4

**R5: Graceful Handling of Off-Topic Input**
- **Problem to Solve:** Employees may ask questions outside the scope of onboarding, which could derail the flow.
- **User Story:** As a new employee, I need the agent to handle unexpected questions politely so that the onboarding flow is not disrupted.
- **Acceptance Criteria:**
  - Given the employee asks an off-topic question, when the agent responds, then it politely acknowledges the question and steers back to the onboarding flow.
- **Maps to Objective:** Objective 1
- **Priority Rank:** 5

---

## Solution Architecture

**Architecture Overview:**
A single Python AI agent built on the A2A protocol, deployed on SAP AI Core. The agent is entirely system-prompt driven — no MCP tools, no external API calls, no workflow integrations. All onboarding logic and content is encoded in the agent's system prompt.

**Key Components:**

- **Greeting & Onboarding Agent (Python, A2A):** Core agent that manages the conversation, collects employee information, delivers onboarding guidance, and confirms completion.
- **System Prompt:** Contains all onboarding steps, tone guidelines, and flow instructions. This is the primary knowledge source.
- **SAP AI Core Runtime:** Hosts and serves the agent using a supported LLM (e.g., GPT-4o via SAP Generative AI Hub).

**Integration Points:**
None. The agent operates fully standalone in this release.

**Deployment Environments:**
- Dev: Development and testing of agent behaviour and prompt refinements
- Prod: Live deployment accessible to new employees

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
The agent is designed to be extended in future releases. Extension points include:
- Adding MCP tool calls to query HR systems (e.g., fetch personalised onboarding checklists per role)
- Injecting additional onboarding modules (e.g., IT setup, compliance training) via prompt or skill additions
- Language support extensions for multilingual onboarding

**Business Step Instrumentation:**
Each of the three key milestones must emit structured log statements to support observability and monitoring in production. See the Milestones section for the exact log patterns.

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent

**Actions the system performs without human approval:**
- Greets the employee and collects name and role
- Delivers onboarding step guidance
- Confirms completion

**Actions that require human review or approval:**
- Updates to onboarding content (managed via system prompt changes, reviewed by HR)

**Model or engine used:** GPT-4o via SAP Generative AI Hub

**Knowledge & data sources accessed:**
- System prompt (onboarding steps, flow logic, tone guidelines) — owned and maintained by HR

**Tools or connectors invoked:**
None. This release is fully self-contained.

**Guardrails & fail-safes:**
- Agent must never claim to perform actions it cannot (e.g., "I have submitted your forms")
- Agent must never ask for sensitive personal data beyond name and role
- If the conversation stalls or the employee is unresponsive, the agent prompts once and then closes gracefully
- Off-topic queries are acknowledged but do not replace onboarding steps

---

## Milestones

### M1: Greeting & Introduction

- **Description:** The agent successfully greets the employee, introduces itself, and collects the employee's name and role.
- **Achieved when:** The employee has provided their name and role, and the agent has acknowledged both.
- **Log on achievement:** `M1.achieved: employee greeted and profile collected — name and role confirmed`
- **Log on miss:** `M1.missed: greeting or profile collection did not complete — conversation may have been abandoned`

### M2: Onboarding Walkthrough

- **Description:** The agent walks the employee through all required onboarding steps in sequence.
- **Achieved when:** The agent has presented and the employee has acknowledged all onboarding steps.
- **Log on achievement:** `M2.achieved: all onboarding steps presented and acknowledged by employee`
- **Log on miss:** `M2.missed: onboarding walkthrough did not complete — one or more steps were not reached`

### M3: Completion Confirmation

- **Description:** The agent confirms that the employee has completed onboarding and is ready to start.
- **Achieved when:** The agent has delivered the final completion message.
- **Log on achievement:** `M3.achieved: onboarding confirmed complete — employee marked as ready to start`
- **Log on miss:** `M3.missed: completion confirmation was not delivered — session may have ended prematurely`

---

## Risks, Assumptions, and Dependencies

### Risks

- **Onboarding content accuracy:** The agent's knowledge is limited to its system prompt. If onboarding steps change and the prompt is not updated, employees receive outdated guidance.
- **LLM response variability:** The agent may occasionally deviate from the intended flow. Prompt engineering and testing must mitigate this.

### Assumptions

- Onboarding steps are stable enough to be encoded in a static system prompt for the initial release.
- Employees have access to the agent via an approved channel (e.g., internal portal or chat interface).
- SAP AI Core and Generative AI Hub are available in the deployment environment.

### Dependencies

- SAP AI Core runtime (for hosting the agent)
- SAP Generative AI Hub (for LLM access — GPT-4o or equivalent)
- HR team availability to define and maintain onboarding step content

---

## Open Questions

- Should the agent support onboarding flows that differ by department or role, or is a single universal flow sufficient for the initial release?
- Who owns the system prompt going forward — HR, IT, or a shared team?
- Is there a target channel or UI through which employees will access the agent (e.g., internal portal, Teams, custom web app)?
