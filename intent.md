# Simple Greeting & Onboarding Agent

## Business challenge

Build a simple AI agent that greets internal employees and guides them through a short onboarding flow conversationally, without any external system integrations.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Onboarding completion time | 3–5 days | 50% faster (1.5–2.5 days) | — | Employee Onboarding | user |

## Key Milestones

1. **Greeting & Introduction** — Agent greets the new employee, introduces itself, and collects the employee's name and role.
2. **Onboarding Walkthrough** — Agent guides the employee through each onboarding step conversationally.
3. **Completion Confirmation** — Agent confirms all steps are done and the employee is ready to start.

## Business Architecture (RBA)

### End-to-End Process

Lead to Cash (Customer domain — managing customer/user experience)

### Process Hierarchy

```
Lead to Cash (E2E)
└── Manage Customers and Channels (generic)
    └── Manage customers (generic) [BPS-370]
        └── Manage customer experience
    └── Manage and operate sales channels (generic) [BPS-371]
        └── Operate omnichannel customer platforms
└── Plan to Optimize Marketing and Sales (generic)
    └── Develop marketing strategy and plans (generic) [BPS-364]
        └── Design and manage customer loyalty program
```

### Summary

A conversational greeting and onboarding agent maps most closely to managing customer/user experience and operating engagement platforms. For the internal-employee use case, this translates to automating the new-hire onboarding conversation without any fixed workflow graph.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|--------------------|--------------------|--------------------|------|---------------------|
| Greet employee and collect basic info | None available | — | — | — | — | — | Yes | Custom agent needed; all discovered APIs are unavailable in this landscape |
| Guide employee through onboarding steps | None available | — | — | — | — | — | Yes | Custom conversational logic in agent system prompt |
| Confirm onboarding completion | None available | — | — | — | — | — | Yes | Handled within agent response flow |

### Key findings

- All APIs discovered (Bot Connector, Conversation Service, etc.) are marked unavailable in this landscape — no MCP integration is needed or possible.
- The solution is a fully custom Python AI agent using the A2A protocol.
- No external data sources or tools are required; the agent operates on its system prompt and conversation context alone.
- The simplicity of the use case means a lightweight agent with a well-crafted system prompt is sufficient.
- OpenTelemetry instrumentation will cover the three key milestones for observability.

## Recommendations

### Simple Greeting & Onboarding AI Agent

#### Executive Summary

Custom Python A2A agent that greets and onboards employees conversationally.

#### Recommended Solution

A pro-code Python agent built on the A2A protocol, deployed on SAP AI Core. The agent uses a carefully crafted system prompt to greet new employees by name, walk them through onboarding steps in a conversational manner, and confirm completion. No MCP servers or external integrations are required.

#### Problem Statement

New employee onboarding currently takes 3–5 days and lacks a guided, interactive experience. Employees must find information across multiple sources, leading to delays and inconsistency.

#### Affected User Roles

- New employees (primary users)
- HR / Onboarding coordinators (indirect beneficiaries)

#### Important factors

##### Reduces time-to-productivity through conversational guidance

The agent walks employees through onboarding steps interactively, eliminating the need to search for information manually.

##### No integration complexity

Since no MCP tools or external APIs are required, the agent is simple to build, test, and maintain.

#### Potential risks

##### Onboarding content accuracy

The agent's knowledge is limited to what is encoded in its system prompt. Outdated or incomplete onboarding instructions will affect quality.

#### Recommended solution category

AI Agent

#### Intent fit
95%
