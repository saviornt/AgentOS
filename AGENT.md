# AgentOS — Agent Operating Guide (for Codex)

This repo is a **local-first agent orchestrator** intended to run inside/alongside Codex, using **MCP servers** to safely access tools (npm/uv/cargo), local apps (Obsidian, UE5), and knowledge/state backends (MongoDB, Redis).

## Design Goals

- **No hallucinated structure**: always read real files before making claims.
- **Policy-gated execution**: only run allowed tool actions (see `policy/`).
- **Local-first memory**:
  - **State** in Redis (what’s in-progress, last actions).
  - **Knowledge** in MongoDB (cached answers, research summaries).
- **Composable integrations** via MCP + app manifests under `apps/`.
- **Docker-friendly** development runtime for dependencies (Redis/Mongo/SearXNG).

## Repo Layout

- `plugin.json` — plugin manifest (skills, MCP config, app manifests, routing).
- `mcp.json` — MCP server definitions (Node + Python servers).
- `mcp/` — Python MCP servers (cargo/npm/uv wrappers + integrations).
- `policy/` — allow-lists for tool execution.
- `routing/skill_router.yaml` — keyword router → skill selection.
- `skills/` — skill prompts/workflows used by the router.
- `state/agent_state.py` — lightweight in-process state shape (optional).
- `apps/` — app manifests (OAuth + permissions declarations).

## Operating Rules (What you, the agent, must do)

1. **Start with the filesystem**
   - Inspect the target project directory (or ask for it) before selecting tools.
   - Prefer `rg`/directory listing over guessing.
2. **Use the orchestrator flow**
   - Check Redis (state) → check Mongo (knowledge) → select tools → execute → persist results.
3. **Obey policies**
   - cargo: `policy/cargo_policy.py`
   - npm: `policy/npm_policy.py`
   - uv: `policy/uv_policy.py`
   - If a requested action is blocked, explain why and propose an allowed alternative.
4. **Prefer MCP tools over raw shell**
   - Use the MCP wrappers for `cargo`, `npm`, and `uv` so policy is enforced consistently.
5. **Be safe by default**
   - No destructive commands (delete/reset) unless explicitly requested and scoped.
   - For UE5 operations, avoid “cleanup” actions unless the project root is clearly correct.

## MCP Servers & Configuration

MCP servers are configured in `mcp.json`.

Common environment variables (from `mcp.json`):

- `SEARXNG_URL` (default: `http://localhost:8081`)
- `AGENTOS_VAULT_PATH` (Obsidian vault root override; default is `~/Documents/Vaults`)
- `REDIS_URL` (default: `redis://localhost:6379`)
- `MONGO_URI` (default: `mongodb://localhost:27017`)
- `MONGO_DB` (default: `agentos`)
- `UE_ENGINE_ROOT` (example: `C:/Program Files/Epic Games/UE_5.7`)
- `UE_PROJECT_ROOT` (UE project folder; must contain a `.uproject`)

## Docker Support (Recommended)

AgentOS expects local services that are ideal to run via Docker:

- Redis (state)
- MongoDB (knowledge)
- SearXNG (research meta-search)

Planned approach:

- Add a `docker-compose.yml` with Redis + Mongo + SearXNG.
- Keep MCP servers running on the host (so they can access the local filesystem, toolchains, UE5, and Obsidian vaults).
- Optionally add a devcontainer to standardize Python/Node tool versions.

If you implement Docker support, ensure:

- Ports are configurable and do not collide with existing services.
- MongoDB data persists via a named volume.
- SearXNG config is mounted and documented.

## Skill Routing

Routing rules live in `routing/skill_router.yaml` and map keywords → skills:

- `agent-orchestrator` for toolchain work (cargo/npm/uv).
- `researcher` for web research via SearXNG.
- `feature-builder` for implementing features.

When a request contains multiple intents (e.g., “research then implement”), do both:
1) run `researcher`, store findings in Mongo, then 2) run `feature-builder`.

## Extending AgentOS

### Add a new MCP server

1. Create a server under `mcp/` (Python) or use an `npx` server.
2. Add it to `mcp.json`.
3. If it executes tools/commands, add an allow-list under `policy/` and enforce it in the MCP server.

### Add a new skill

1. Add a markdown skill file under `skills/`.
2. Register it in `plugin.json` under `skills`.
3. Add router rules in `routing/skill_router.yaml`.

### Add a new “app”

1. Add a manifest under `apps/` describing auth + permissions.
2. Register it in `plugin.json` under `apps`.

## Known Gaps / Things to Confirm

- **Docker scope**: should Docker run only Redis/Mongo/SearXNG, or also containerize the MCP servers?
- **SearXNG**: confirm desired image/config, language defaults, and whether outbound internet access is required.
- **Obsidian vault layout**: confirm the expected vault name(s) and whether multi-vault usage is needed.
- **UE5 safety**: `mcp/ue5_server.py` includes a cleanup helper; confirm the intended deletion semantics and platform support.

