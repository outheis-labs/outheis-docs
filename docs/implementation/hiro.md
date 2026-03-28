---
title: Hiro
---

# Hiro

*External action agent — not yet implemented.*

## What hiro does

hiro is outheis's action agent. Where zeno searches the vault and cato manages time, hiro acts on the outside world: sending email, updating calendars, triggering external services.

**hiro is present in the current release but has no capabilities.** The agent starts, routes messages, and responds, but no external integrations exist yet. Enabling it in `config.json` has no practical effect.

## Planned Architecture

hiro will be built as an **MCP client**. Rather than implementing integrations directly in outheis, hiro connects to external MCP servers — one per service — and exposes their tools through the standard agent interface.

### Why MCP

Model Context Protocol provides a standardized interface between LLMs and external tools. The MCP server ecosystem already covers many common integrations (email, calendar, browser, shell). Building hiro as an MCP client means:

- No integration code lives in outheis itself
- New capabilities are added by configuring a server, not by writing code
- Each server runs as an isolated process with its own permissions

### Server Lifecycle

MCP servers run as subprocesses managed by the dispatcher. hiro does not manage server lifecycle directly — the dispatcher starts configured servers at launch, monitors them, and restarts them if they exit. hiro connects to already-running servers.

Two modes are planned:

| Mode | Behavior |
|------|----------|
| Persistent | Server runs continuously alongside the dispatcher |
| On-demand | Server is started when hiro needs it, stopped after a configurable idle timeout |

### Curated Server List

hiro will not accept arbitrary MCP server configurations. Supported servers are maintained in a curated list that records which server was tested, against which version, and when. A server appears in the list only after it has been verified to work correctly with outheis.

This is a deliberate constraint. The MCP ecosystem is large and uneven — quality varies significantly. A whitelist approach means you know exactly what hiro can do and that it works.

The list will be maintained in the outheis repository and updated as servers are tested.

### Configuration

When implemented, hiro's servers will be configured in `config.json`:

```json
{
  "agents": {
    "action": {
      "enabled": true,
      "servers": [
        {"name": "gmail",  "command": "npx", "args": ["-y", "@modelcontextprotocol/server-gmail"]},
        {"name": "gcal",   "command": "npx", "args": ["-y", "@modelcontextprotocol/server-gcal"]}
      ]
    }
  }
}
```

Only servers on the curated list will be accepted. Unknown servers are ignored with a warning at startup.

## Current Status

| Component | Status |
|-----------|--------|
| Agent shell (routing, dispatch) | ✓ present |
| MCP client | not implemented |
| Server lifecycle management | not implemented |
| Curated server list | not started |
| Any external integration | not implemented |
