# AgentEx

AgentEx is a **Codex plugin-based agent orchestration layer** that provides structured **skills, MCP tool integrations, and application connectors** for agentic workflows across development, research, and personal automation.

---

## Overview

AgentEx acts as a **bridge between Codex and your local/remote tooling stack**, enabling structured agent workflows through:

* **Skills** → reusable behavioral instructions for Codex
* **MCP servers** → tool execution layer (system, apps, memory, external services)
* **Apps** → external service integrations (e.g., GitHub, Google Drive)
* **Policies** → execution constraints and safety rules per tool domain
* **Routing layer** → maps intent → skill → tool execution
* **State layer** → persistent + ephemeral agent memory

---

## Architecture

AgentEx is composed of five primary layers:

### 1. Codex Plugin Layer

Defined in:

* `plugin.json`
* `AGENT.md`
* `.mcp.json`

This layer exposes AgentEx to Codex as a plugin, registering:

* skills
* MCP tool servers
* app integrations

---

### 2. Skills Layer (Behavior System)

Defined in:

* `skills/*.md`
* `routing/skill_router.yaml`

Skills define **how Codex should behave in different contexts**, such as:

* `agent-orchestrator` → system-level task coordination
* `dev-cycle` → software development workflow loop
* `researcher` → structured information gathering
* `knowledge-first` → retrieval + synthesis workflows

Skills are **prompt-level execution policies**, not runtime code.

---

### 3. MCP Tooling Layer (Execution System)

Defined in:

* `mcp/*.py`

MCP servers expose structured tool interfaces to Codex:

| Domain          | MCP Server               |
| --------------- | ------------------------ |
| Rust tooling    | cargo_server.py          |
| Node tooling    | npm_server.py            |
| Python env      | uv_server.py             |
| Unreal Engine 5 | ue5_server.py            |
| Obsidian        | obsidian_agent_server.py |
| Redis memory    | redis_memory_server.py   |
| MongoDB memory  | mongo_memory_server.py   |

This layer provides AgentEx with **real system execution capability**.

---

### 4. Policy Layer (Execution Constraints)

Defined in:

* `policy/*.py`

Policies enforce domain-specific rules for tool execution:

* npm safety constraints
* cargo build rules
* uv environment restrictions

This layer ensures tool usage remains:

* deterministic
* safe
* scoped
* workflow-aware

---

### 5. State & Memory Layer

Defined in:

* `state/agent_state.py`
* `redis_memory_server.py`
* `mongo_memory_server.py`

Memory is split into:

* **Redis** → short-term / working memory
* **MongoDB** → persistent structured memory

This enables AgentEx to maintain:

* session continuity
* long-term context retention
* workflow state tracking

---

## Apps Layer

Defined in:

* `apps/github.app.json`
* `apps/google-drive.app.json`

Apps represent external service integrations, such as:

* GitHub (repo + issue automation)
* Google Drive (document and file access)

These are exposed through MCP-style tool interfaces.

---

## Workflow Model

AgentEx follows a structured execution pipeline:

```
User Input
   ↓
Skill Router (skill_router.yaml)
   ↓
Skill Behavior (SKILL.md)
   ↓
Policy Validation
   ↓
MCP Tool Execution
   ↓
State Update (Redis / Mongo)
   ↓
Response via Codex
```

This allows deterministic orchestration of agent behavior while maintaining flexibility in tool usage.

---

## Key Design Principles

### 1. Tool-first architecture

AgentEx does not simulate tools — it executes real ones via MCP servers.

### 2. Skill-driven behavior

Behavior is modularized into skills instead of hardcoded prompts.

### 3. Policy-aware execution

Every tool invocation can be constrained or modified by policy rules.

### 4. Multi-memory system

Short-term + long-term memory separation for structured agent continuity.

### 5. Codex-native integration

AgentEx is designed as a **Codex plugin**, not a standalone runtime.

---

## Intended Use Cases

AgentEx is designed for:

* Development automation (build, test, deploy workflows)
* Research and knowledge synthesis pipelines
* Local-first AI orchestration
* UE5 + creative production workflows
* Personal productivity automation
* Cross-tool agent coordination (filesystem, cloud, memory)

---

## Not a Standalone OS

AgentEx is:

* a Codex plugin
* a tool orchestration layer
* a skills + MCP execution framework

It is NOT:

* a kernel
* a standalone agent runtime
* an operating system replacement

---

## Project Structure

```
plugin.json              → Codex plugin manifest
AGENT.md                → agent behavior instructions
mcp.json                → MCP server registry

mcp/                    → execution servers
skills/                → behavior modules
routing/               → skill routing logic
policy/                → execution constraints
apps/                  → external integrations
state/                 → agent memory layer
```

---

## Summary

AgentEx provides a **modular Codex plugin system** that connects:

* skills (behavior)
* MCP servers (execution)
* apps (integrations)
* policies (constraints)
* memory (state)

into a unified agentic workflow layer for development and automation tasks.

---

If you want next step, I can tighten this into:

* a **professional GitHub README with badges + diagrams**
* or a **“Codex Marketplace ready” plugin description version**
* or a **technical architecture doc (with diagrams + execution flow state machine)**
